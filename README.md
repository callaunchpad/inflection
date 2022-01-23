# Overview

Ever wanted to turn Alexa in Spongebob’s voice? Inflection is a framework to train, test, and deploy voice conversion models for voice assistants. Based on supervised ML using Mel-Frequency Cepstral Coefficients, it provides a simple way to generate data, perform spectral analysis, create models, and serve them through a web app. All you need as input is a 10-15 minute MP3 of someone talking!

The data flow is described here and further details are provided within folder README files. A sample implementation for Ivanka Trump’s voice is also completed in the research section.

![Process Overview](https://github.com/mraheja/inflection/blob/main/ProcessOverview.png)

# Environment 

We recommend that you create a virtual conda environment in Python 3.6.9. To do so and install all the required packages, run: 

```
conda create -n myenv python=3.6
conda activate myenv
pip install -r requirements.txt
```

# Sections

[Data Generation]
[Spectral Analysis]
[Model Training]
[Webapp]
[Research]
