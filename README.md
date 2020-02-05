# Product Dashboard

<p align="center">
  <img width="460" height="300" src="src/product_dashboard.gif">
</p>

[Product Dashboard](github.com/kludex/product_dashboard) is a
[dash](https://dash.plot.ly/) application created to analyze different products.
This analysis process is made based on forecasting predictions. Also, for each
product we have the best, the worst and the base possible prediction results.

## Installation

To be able to run this project, we recommend to use a
[conda](https://docs.conda.io/en/latest/).

First, we're gonna clone the repository, then create the environment.
```
git clone https://github.com/Kludex/product_dashboard
cd product_dashboard/

conda env create -f environment.yml
```

Check if the environment was created:
```
conda env list
```

## Usage

Now that we have all the dependencies installed, run the application:
```
python app.py
```

Then, go to your favorite browser and paste the following link
[http://127.0.0.1:8050/](http://127.0.0.1:8050/) (or just click on it).

## What's Missing?

- [ ] Option dropdown width adjust.
- [ ] Block outlier interval if there's no change in the plot values.
- [ ] Add the option to download a csv file.
- [ ] Default outlier should be the one that makes the curve more friendly to
  the human eyes.
- [ ] Tests.
- [ ] Use linter on the `app.py` file. It was not added because it has a HTML structure inside which breaks some linter rules that we don't want to ignore, as line limit.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This code was made as part of the [Funcional Corp] technical challenge. If
requested by them, this repository will be turn to private. If not, I will add a
open source license.