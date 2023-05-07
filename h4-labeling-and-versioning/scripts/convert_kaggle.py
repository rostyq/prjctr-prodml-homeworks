from pathlib import Path


def convert_session(src: Path, dest: Path):
    from csv import DictReader, DictWriter

    # pid, activity = src.name.split("_")

    snapshots = []
    with src.open("r") as f:
        for row in DictReader(f):
            time = int(row["timestamp"]) / 1000
            x, y = int(row['x']), int(row["y"])
            snapshots.append({"time": time, "x": x, "y": y})
    
    out = dest / src.name
    
    with out.open("w") as f:
        writer = DictWriter(f, ["time", "x", "y"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(snapshots)


def main(dataset_path: Path, output_path: Path):
    from tqdm import tqdm

    for path in tqdm(dataset_path.glob("*.csv")):
        convert_session(path, output_path)


if __name__ == "__main__":
    from typer import run

    run(main)