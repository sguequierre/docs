---
title: "Microcontroller Setup: the Micro-RDK"
linkTitle: "Microcontroller Setup"
weight: 50
no_list: true
type: docs
image: "installation/thumbnails/esp32-espressif.png"
imageAlt: "E S P 32 - espressif"
images: ["/installation/thumbnails/esp32-espressif.png"]
description: "Set up the Espressif ESP32 with the micro-RDK."
aliases:
    - /installation/microcontrollers
# SMEs: Nicolas Menard
---

{{% readfile "/static/include/micro-rdk.md" %}}

## Get Started

To install and build the `micro-rdk` on your ESP32 board, follow these steps:

1. Install the [required software](#software-requirements)
2. [Set up your development enviroment](#set-up-your-docker-development-enviroment) with Viam's [Canon CLI utility](#use-viams-canon-cli-utility) *(recommended)* or [manually](#set-up-development-environment-manually)
3. [Install the Micro-RDK](#install-the-micro-rdk)

### Hardware Requirements

You need an an Espressif ESP32 microcontroller to use the micro-RDK.
Viam recommends purchasing the ESP32 with a development board: see [development kit options](https://www.espressif.com/en/products/devkits).

- **Minimal configuration:** 384kB Ram 4MB flash
- **Recommended configuration:** 384kB Ram + 8MB SPIRAM + 4MB Flash

### Software Requirements

The micro-RDK is written in Rust.
The following instructions cover installation of necessary tools to program the ESP32 on macOS and Linux systems.

To build the micro-rdk, you must install the following software on your development machine:

#### Install Build Dependencies

{{< tabs >}}
{{% tab name="Linux (Ubuntu)" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt-get install git libssl-dev dfu-util libusb-1.0-0 libudev-dev
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew install dfu-util
```

{{% /tab %}}
{{% /tabs %}}

#### Install `Rust`

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

See the [Rust Installation guide](https://www.rust-lang.org/tools/install) for more information and other installation methods.

#### Install `cargo-generate` with `cargo`

 `cargo` installs automatically when downloading Rust with rustup.

Run the following command to install `cargo-generate`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo install cargo-generate
```

#### Install `espflash`

Run the following command to install `espflash`

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo install espflash
```

## Set up your Docker development enviroment

### Use Viam's Canon CLI utility

[Canon](https://github.com/viamrobotics/canon) is a CLI utility for managing a Docker based canonical environment.

Canon requires a working installation of Docker.

[Install Docker](https://docs.docker.com/engine/install/) before proceeding.
If you are running Docker on Linux, make sure that you go through the [post installation steps](https://docs.docker.com/engine/install/linux-postinstall/).

{{< tabs >}}
{{% tab name="Linux (Ubuntu)" %}}

Go 1.19 or newer must be installed.

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
go install github.com/viamrobotics/canon@latest
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew install viamrobotics/brews/canon
```

{{% /tab %}}
{{% /tabs %}}

Make sure to [add the go binary folder to your `PATH`](https://go.dev/ref/mod#go-install).

### Set up development environment manually

{{< alert title="Tip" color="tip" >}}
You only need to follow these steps if you are not using Canon to build the micro-RDK.

If you have completed [set up with Canon](/installation/prepare/microcontrollers/#use-viams-canon-cli-utility), skip this section and begin on [install the Micro-RDK](/installation/prepare/microcontrollers/#install-the-micro-rdk).

{{< /alert >}}

To set up the Docker development environment for ESP manually, complete the following:

{{%expand "Install build dependencies" %}}

{{< tabs >}}
{{% tab name="Linux (Ubuntu)" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
brew install cmake ninja dfu-util
```

{{% /tab %}}
{{% /tabs %}}

{{% /expand%}}

{{%expand "Install ESP-IDF" %}}

ESP-IDF is the development framework for Espressif SoCs (System-on-Chips), supported on Windows, Linux and macOS.

Clone Viam's fork of the ESP-IDF:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
mkdir -p ~/esp
cd ~/esp
git clone --depth 1 -b v4.4.4 --single-branch --recurse-submodules --shallow-submodules https://github.com/npmenard/esp-idf
```

Then, install the required tools for ESP-IDF:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cd ~/esp/esp-idf
./install.sh esp32
```

To activate ESP-IDF, run the following command to source (`.`) the activation script `export.sh`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
. $HOME/esp/esp-idf/export.sh
```

To avoid conflicts with other toolchains, adding this command to your `.bashrc` or `.zshrc` is not recommended.
Save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.

{{% /expand%}}

{{%expand "Install the Rust ESP Toolchain and Activate the ESP-RS Virtual Environment" %}}

First install the following tools with `cargo` :

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo install espup
```

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo install cargo-espflash v2.0.0-rc.1
```

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo install ldproxy
```

Finally to download and install the esp-rs toolchain run :

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
espup install -s -f ~/esp/export-rs.sh -v 1.67.0
```

To activate the ESP Rust toolchain, run the following command to source (`.`) the activation script `export-rs.sh`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
. $HOME/esp/esp-idf/export-rs.sh
```

To avoid conflicts with other toolchains, adding this command to your `.bashrc` or `.zshrc` is not recommended.
Save this command to run in any future terminal session where you need to activate the ESP Rust development framework.

{{% /expand%}}

## Install the Micro-RDK

### Create a New Robot

Navigate to [the Viam app](https://app.viam.com) and create a new robot in your desired location.
Keep your `Mode` and `Architecture` selections at default, and skip the instructions in the **Setup** tab for now as the setup instructions there are not for microcontrollers.
You can configure your robot using the config tab.

{{< alert title="Caution" color="caution" >}}
As of the time this guide is written the esp32 board component doesn't exist yet on app.viam.com below you can find the board template for esp32:

```json
{
  "attributes": {
    "webhook": "", // Optional path a webhook see https://github.com/viam-labs/webhook-template for an example
    "webhook-secret": "", // Option webhook secret
    "pins": [ // pin to be configured as Input/Ouput (for Get/SetGpio)
      15
    ],
    "analogs": [
      {
        "pin": "34", // analog pins
        "name": "sensor"
      }
    ]
  },
  "depends_on": [],
  "model": "esp32",
  "name": "board",
  "type": "board"
}
```

{{% /alert %}}

### Generate a New Project from the Micro-RDK Template

Use [the micro-RDK template](https://github.com/viamrobotics/micro-rdk-template.git) to create a new micro-RDK project to upload to your ESP32 by running:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
cargo generate --git https://github.com/viamrobotics/micro-rdk-template.git
```

To track any changes you make to the generated project with Git, use the `mkdir` command to initialize a new repository inside of the directory you created by running `cargo-generate`.

You will be prompted to paste your robot's JSON configuration into the terminal.

To obtain this, navigate to [the Viam app](https://app.viam.com).
Click the **Copy viam-server config** button on the right side of the **Setup** tab of your robot.
The micro-RDK needs this JSON file, which contains your robot part secret key and cloud app address, to connect to [the Viam app](https://app.viam.com).
Paste your JSON config into your terminal when prompted.

{{% snippet "secret-share.md" %}}

### Upload and Connect to your ESP32 Board

{{< tabs >}}
{{% tab name="Using Canon" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
canon bash -lc "make build-esp32-bin"
make flash-esp32-bin
```

{{% /tab %}}
{{% tab name="Local environment" %}}

Make sure you have run `. ~/dev/esp/export-rs.sh` and `. ~/dev/esp/esp-idf/export.sh` before running the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
make upload
```

{{% /tab %}}
{{% /tabs %}}

If successful you will retain a serial connection to the board until `Ctrl-C` is pressed.
To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

If everything went well, your ESP32 is now programmed so that you will be able to see your robot live and connect to it on [the Viam app](https://app.viam.com).

### Troubleshooting

If you run into the error `Failed to open serial port` when flashing your ESP32 with Linux, make sure the user is added to the group `dialout` with `sudo gpasswd -a $USER dialout`

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
