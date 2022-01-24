# Research

This section outlines a series of attempts to complete voice conversion, observations made throughout the process, and results of various models. The example code for the final attempt, the BiLSTM, can be found under the `code` folder.

## Human-to-Human Voice Conversion

Before creating our voice-converted assistant, we decided to experiment with models on human-to-human voice conversion. The first reason for this was that there was clear, easy to use . Second, this is a much better studied problems so there are years of research for us to draw upon 

### Linear Regression

As a baseline, we used sklearn to quickly train a linear regression model on the MFCCs. Even on the CPU, this trained on the entirety of data within seconds and we had some basic voice conversion going, although the output was very clearly robotics.

**Results:**

[Example Input]() \
[Example Output]()

### Multi-Layer Perceptron (MLP)

**Results:**

[Example Input]() \
[Example Output]()

### Recurrent Neural Network (RNN)

**Results:**

[Example Input]() \
[Example Output]()

## Assistant-to-Human Voice Conversion

With human-to-human voice conversion performing quite well, we decided to attempt our actual goal: real time assistant-to-human voice conversion. This posed a variety of new challenges and turned out to be a significantly more difficult problem. Some of the major new difficulties were:

Accordingly, re-using the RNN architecture from human-to-human voice conversion performed quite poorly. Although we still had a relative low amount of data, we had to move forward by using more complex models.

### Long Short-Term Memory (LSTM)

**Results:**

[Example Input]() \
[Example Output]()

### Bi-directional Long Short-Term Memory (BiLSTM)

**Results:**

[Example Input]() \
[Example Output]()

## Overall Results


These results can also be found in our presentation [here](https://docs.google.com/presentation/d/1nLFZPVwVGFXDhbRbeFxIbF5qrEZdSSqoMhxTUgtZWqs/edit#slide=id.g105783f6fe8_13_2)
