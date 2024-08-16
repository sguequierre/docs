---
title: "Collect and view sensor data from any machines"
linkTitle: "Collect sensor data"
weight: 29
type: "docs"
images: ["/services/icons/data-capture.svg"]
description: "Gather sensor data, sync it to the cloud, and view it in the Viam app."
modulescript: true
aliases:
  - /use-cases/collect-sensor-data/
# SME: Devin Hilly
---

You can use the data management service to capture sensor data from any or all of your machines and sync that data to the cloud.
For example, you can configure data capture for several sensors across one or multiple machines to report the current memory usage or the ambient operating temperature.

You can do all of this using the [Viam app](https://app.viam.com/) user interface.
You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Gather data on any machine and syncing it to the cloud](#gather-and-sync-data).
1. [View sensor data](#view-sensor-data).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "At least one configured sensor. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a sensor model](/components/sensor/) that supports your sensor.

If you're not sure which sensor model to choose, add the `viam:viam-sensor:telegrafsensor` which captures performance data (CPU, memory usage, and more) from your machine. After adding the component, use the following attribute configuration:

```json {class="line-numbers linkable-line-numbers"}
{
  "disable_cpu": false,
  "disable_disk": false,
  "disable_disk_io": false,
  "disable_kernel": false,
  "disable_mem": false,
  "disable_net": false,
  "disable_netstat": false,
  "disable_processes": false,
  "disable_swap": false,
  "disable_system": false,
  "disable_temp": true,
  "disable_wireless": true
}
```

{{% /expand%}}

## Gather and sync data

Viam's [data management service](/services/data/) lets you capture data locally from sensors and then sync it to the cloud where you can access all data across different {{< glossary_tooltip term_id="machine" text="machines" >}} or {{< glossary_tooltip term_id="location" text="locations" >}}.

{{< table >}}
{{% tablestep link="/services/data/"%}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
**1. Add the data management service**

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Then add the **data management** service.

Enable **Syncing** to ensure captured data is synced to the cloud and set the sync interval, for example to `0.05` minutes to sync every 3 seconds.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/icons/components/sensor.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="configure a camera component">}}
**2. Capture data from sensor**

On the **CONFIGURE** tab, go to the **sensor**'s card and find the **Data capture** section.
Add a new method, `Readings`, to capture data for and set the frequency.
For example, setting a frequency of `0.1` will capture data once every ten seconds.

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/services/ml/configure.svg" class="fill alignleft" style="max-width: 150px"  declaredimensions=true alt="Train models">}}
**3. Save to start capturing**

Save the config.
With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

{{% /tablestep %}}
{{< /table >}}

{{< alert title="Tip" color="tip" >}}
If you need to sync data conditionally, for example at a certain time, see [Trigger Sync](/services/data/trigger-sync/#configure-data-manager-to-sync-based-on-sensor).
{{< /alert >}}

## View sensor data

{{< table >}}
{{% tablestep link="/services/data/view/"%}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Capture tabular data from a sensor">}}
**1. View data in the Viam app**

To confirm data is being synced, go to the **DATA** tab and select the **Sensors** subtab.
Confirm that you are seeing data appear.

![Sensor data tab](/get-started/quickstarts/collect-data/data-page.png)

{{% /tablestep %}}
{{< /table >}}

## Next steps

Now that you have collected sensor data, you can [query it](/how-tos/sensor-data-query-with-third-party-tools/), [access it programmatically](/how-tos/sensor-data-query-sdk/) or [visualize it](/how-tos/sensor-data-visualize/) with third-party tools.

{{< cards >}}
{{% card link="/how-tos/sensor-data-query-with-third-party-tools/" %}}
{{% card link="/how-tos/sensor-data-query-sdk/" %}}
{{% card link="/how-tos/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}