# Webapp

The webapp serves the model trained in [Model Training] onto a simple voice assistant web interface.

## Setup

For setup, open the `ml.py` file and replace the `predict` function with the predict function you created in [Model Training]. Note that if you have model weights saved, you should transfer them from the `model_training` folder to this one then import them at the start of `ml.py`.

## Run

To run the app, run:

```
python app.py
```

After this, visiting whichever `localhost` url that Flask provides will open up the webpage and you will immediately be able to interact with the model!