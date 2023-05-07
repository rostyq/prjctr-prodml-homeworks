# H4 Labeling & Versioning

### DVC

Setup Minio and its keys:

```ps1
$env:AWS_ACCESS_KEY_ID="minioadmin"
$env:AWS_SECRET_ACCESS_KEY="minioadmin"
```

Create bucket and add it to dvc:

```
aws s3 create-bucket --bucket dvc-store --endpoint-url http://localhost:9000
dvc remote add --default minio s3://dvc-store
```

Push commited data:

```
dvc push
```


## Label studio

### Run studio

```
docker run -it -p 8080:8080 -v label-studio:/label-studio/data heartexlabs/label-studio:latest
```

### Labeling setup

```jsx
<View>
  <TimeSeriesLabels name="label" toName="ts">
    <Label value="F-pattern" background="red"/>
    <Label value="Commitment pattern" background="green"/>
    <Label value="Layer-cake pattern" background="blue"/>
    <Label value="Spotted pattern" background="#f6a"/>
  </TimeSeriesLabels>

  <TimeSeries
        name="ts"
        valueType="url"
        value="$timeseriesUrl"
        sep=","
        timeColumn="time"
        fixedScale="true"
        overviewChannels="x,y">

    <Channel
        column="x"
        units="pixels"
        displayFormat=",.1f"
        strokeColor="#1f77b4"
        legend="Gaze X" />
    <Channel
        column="y"
        units="pixels"
        displayFormat=",.1f"
        strokeColor="#ff7f0e"
        legend="Gaze Y" />
  </TimeSeries>
</View>
```
