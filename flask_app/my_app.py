# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi -


from flask_app import create_app, config

app = create_app(config.DevelopmentConfig)

if __name__ == '__main__':
    app.run()
