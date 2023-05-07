from pathlib import Path


def load_participants(root: Path) -> list[dict]:
    from csv import DictReader

    path = root.joinpath("participant_characteristics.csv")
    with path.open("r") as f:
        participants = [row for row in DictReader(f)]

    participants.sort(key=lambda p: int(p["Participant ID"].split("_")[1]))
    return participants


def load_snapshots(root: Path, participant: dict) -> list[dict]:
    from contextlib import suppress
    from json import loads, JSONDecodeError

    pid = participant["Participant ID"]
    path = root.joinpath(pid).joinpath(pid).with_suffix(".txt")

    snapshots = []
    with path.open("rb") as f:
        for line in f.readlines():
            with suppress(JSONDecodeError):
                snapshots.append(loads(line))

    snapshots.sort(key=lambda snapshot: snapshot["true_time"])
    return snapshots


def convert_and_write_snapshots(participant: dict, snapshots: list[dict], dest: Path):
    from csv import DictWriter

    pid = participant["Participant ID"]

    display_width = int(participant["Display Width (pixels)"])
    display_height = int(participant["Display Height (pixels)"])

    timestamp_origin = snapshots[0]["true_time"]

    path = dest.joinpath(pid).with_suffix(".csv")

    with path.open("w") as f:
        writer = DictWriter(f, ["time", "x", "y"], lineterminator="\n")
        writer.writeheader()

        for snapshot in snapshots:
            if snapshot["right_gaze_point_validity"] == 1:
                side = "right"
            elif snapshot["left_gaze_point_validity"] == 1:
                side = "left"
            else:
                continue

            x, y = snapshot[f"{side}_gaze_point_on_display_area"]

            writer.writerow(
                {
                    "time": snapshot["true_time"] - timestamp_origin,
                    "x": int(x * display_width),
                    "y": int(y * display_height),
                }
            )


def process_participant(participant: dict, input: Path, output: Path):
    convert_and_write_snapshots(
        participant=participant,
        snapshots=load_snapshots(root=input, participant=participant),
        dest=output,
    )


def main(dataset_path: Path, output_path: Path):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    from tqdm import tqdm

    participants = load_participants(dataset_path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        with tqdm(total=len(participants), desc="participants") as pbar:
            futures = [
                executor.submit(
                    process_participant,
                    participant=participant,
                    input=dataset_path,
                    output=output_path,
                )
                for participant in participants
            ]

            for _ in as_completed(futures):
                pbar.update(1)


if __name__ == "__main__":
    from typer import run

    run(main)
