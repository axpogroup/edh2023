# edh2023
Thanks for choosing Axpo's challenge, **Predicting Voltages in Substations**, for the Energy Data Hackdays 2023. We're glad you're here!

## Getting Started

This README will guide you through the process of setting up your environment and working on the challenge. By the end of this guide, you'll be ready to dive into the provided datasets, create your predictive model, and help us improve grid stabilization.

### Prerequisites

Before you begin, please ensure you have the following prerequisites:

1. **Access to the VM with Jupyter Hub:** We've provided a virtual machine with Jupyter Hub installed. This will serve as your development environment. Just go to our [Jupyter Hub](http://axe-lab-appl-energy-data-hackdays.westeurope.cloudapp.azure.com/hub) and sign in with a username (no special characters or spaces) and password of your choosing - just don't forget it.

You can also develop on your local machine if you prefer. In this case you can download the training data from our [onedrive](https://axpogrp.sharepoint.com/:f:/s/CMTYTOMDigitalAssetSolutions-MTA/Egl90FJJk3hPqqRx8VOa690Bv86Iz06FaFBMdVxu_jH0UA?e=msOiL1) <span style="color:red">TODO: make a link that is accessible without Axpo credentials</span>.

### Setting Up Your Environment

Follow these steps to set up your environment and start working on the challenge:

1. **Access Jupyter Hub:**
Open your web browser and navigate to the provided URL for Jupyter Hub. Log in using your credentials.

2. **Clone the Git Repository:**
Open a terminal and clone this repo
```console
git clone https://github.com/axpogroup/edh2023.git
cd edh2023
```

3. **Accessing Datasets:**
The training and validation datasets for both substations are located in the `/data` directory on the Jupyter Hub VM. You can copy them to the data directory with 
```console
cp /home/data/* ./data
```

4. **Installing Dependencies:**
Create a virtual environment to install dependencies:
```console
python -m venv .venv
```
Activate the virtual environment
```console
source .venv/bin/activate
```
To ensure your environment has the necessary packages, run the following command:
```console
pip install -r requirements.txt
```
Register the virtual environment as ipykernel:
```console
python -m ipykernel install --user --name=edh_venv
```
It will take a few seconds for the new environment to show up as an available. You can open the `sample_notebook.ipynb` and select the environment as kernel once it is and get going with digging into the details.
### Understanding the Challenge

Before you start coding, it's important to grasp the problem at hand:

- You are provided with time series of substation measurements, energy production, weather data, and target voltages for two substations with shunt reactors.

- The goal is to create a model that can predict voltages in the substation such that, based on these predictions, one can decide when to turn the shunt reactors on or off to keep the measured voltage close to the target voltage. You should keep the average **number of on-off/off-on switches below 2/day** to limit wear and tear on system components. One of the main challenges herein is

### Your Task

Your main task is to develop a predictive model that predicts the voltage in each substation and that can effectively recommend when to activate or deactivate shunt reactors in order to stabilize the grid voltages. Use the provided datasets to train and validate your model. They contain weather, electricity production, and grid measurement data. Take a look at the `sample_notebook.ipynb` to get started with analyzing the data.

Feel free to explore different machine learning algorithms, techniques, and preprocessing methods. Don't hesitate to innovate and experiment!

### Evaluation

You can evaluate your model with either the root mean square error for the voltage prediction or `utils.eval.alternative_strategy_reward`. Both of these are relevant metrics for us.

## Need Help?

If you encounter any issues during the challenge or have questions about the provided datasets, feel free to ask one of us for help. 

Happy coding!
