import matplotlib.pyplot as plt
import pandas as pd


def plot_model_results(confirmed_predicted, confirmed, deaths_predicted, deaths):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

    ax1.set_title('Infected')
    ax2.set_title('Deaths')

    pd_df_predicted = pd.DataFrame({'Infected': confirmed_predicted, 'Deaths': deaths_predicted})
    pd_df_train = pd.DataFrame({'Infected': confirmed.iloc[0], 'Deaths': deaths.iloc[0]})

    pd_df_predicted['Infected'].plot(label='Infected (predicted)', color='g', ax=ax1)
    pd_df_train['Infected'].plot(label='Infected', color='r', ax=ax1)

    pd_df_predicted['Deaths'].plot(label='Deaths (predicted)', color='g', ax=ax2)
    pd_df_train['Deaths'].plot(label='Deaths', color='r', ax=ax2)

    ax1.legend(loc='best')
    ax2.legend(loc='best')

    plt.show()

    ax1.legend(loc='best')


def plot_model_prediction(confirmed_predicted, deaths_predicted):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

    ax1.set_title('Infected')
    ax2.set_title('Deaths')

    pd_df_predicted = pd.DataFrame({'Infected': confirmed_predicted, 'Deaths': deaths_predicted})

    pd_df_predicted['Infected'].plot(label='Infected (predicted)', color='g', ax=ax1)

    pd_df_predicted['Deaths'].plot(label='Deaths (predicted)', color='g', ax=ax2)

    ax1.legend(loc='best')
    ax2.legend(loc='best')

    plt.show()

    ax1.legend(loc='best')


def plot_model_prediction_all(prediction):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    legend = []
    for key, value in prediction.items():
        ax1.plot(value)
        legend.append(key)
    plt.legend(legend)

    plt.show()
