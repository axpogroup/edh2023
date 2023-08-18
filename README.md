# edh2023
Thanks for choosing Axpo's challenge - **Predicting Voltages in Substations** for the Energy Data Hackdays 2023. We're glad you're here!

## Getting Started

This README will guide you through the process of setting up your environment and working on the challenge. By the end of this guide, you'll be ready to dive into the provided datasets, create your predictive model, and help us improve grid stabilization.

### Prerequisites

Before you begin, please ensure you have the following prerequisites:

1. **Access to the VM with Jupyter Hub:** We've provided a virtual machine with Jupyter Hub installed. This will serve as your development environment. Just go to our [Jupyter Hub](jupyterhub.com) and sign in with a username (no characters or spaces) and password of your choosing.

### Setting Up Your Environment

Follow these steps to set up your environment and start working on the challenge:

1. **Clone the Git Repository:**
Open a terminal and clone this repo
```console
git clone <repository_url>
cd edh2023
```

2. **Access Jupyter Hub:**
Open your web browser and navigate to the provided URL for Jupyter Hub. Log in using your credentials.

3. **Accessing Datasets:**
The training and validation datasets for both substations are located in the `/data` directory on the Jupyter Hub VM. You can copy them to the data directory with 
```console
cp /data/* data
```

4. **Installing Dependencies:**
Create a virtual environment to install dependencies:
```console
python -m venv .venv
```
Activate it on windows
```console
.venv\Scripts\activate
```
or on linux/macOS
```console
source .venv/bin/activate
```
To ensure your environment has the necessary packages, run the following command in a Jupyter Notebook cell which uses the .venv as kernel:

```console
!pip install -r requirements.txt
```

### Understanding the Challenge

Before you start coding, it's important to grasp the problem at hand:

- You are provided with time series measurements and target voltages for two substations with shunt reactors.

- The goal is to create a model that can determine when to turn the shunt reactors on or off to minimize wear and tear while keeping the voltage as close as possible to the target voltage. You should keep the average **number of on-off/off-on switches below 2/day** to limit wear and tear on system components.

### Your Task

Your main task is to develop a predictive model that can effectively make decisions about when to activate or deactivate shunt reactors in order to stabilize the grid voltages. Use the provided datasets to train and validate your model.

Feel free to explore different machine learning algorithms, techniques, and preprocessing methods. Don't hesitate to innovate and experiment!

### Submission

Once you've developed your model, it's time to submit your solution. In the root directory of your cloned repository, create a subdirectory named `submission`. Place your trained model and any necessary code files within this directory.

## Need Help?

If you encounter any issues during the challenge or have questions about the provided datasets, feel free to reach out for assistance. 

Happy coding!
