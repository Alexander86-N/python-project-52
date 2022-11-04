### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alexander86-N/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Alexander86-N/python-project-52/actions)
[![example workflows](https://github.com/Alexander86-N/python-project-52/actions/workflows/myci.yml/badge.svg)](https://github.com/Alexander86-N/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/a5bb3cbe48daee9260ff/maintainability)](https://codeclimate.com/github/Alexander86-N/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a5bb3cbe48daee9260ff/test_coverage)](https://codeclimate.com/github/Alexander86-N/python-project-52/test_coverage)

# Task Manager

This is a new project of my studies.
View the work of the Task Manager on [Heroku](https://mysterious-bastion-77076.herokuapp.com/)

## How to install and use

### Install
```
git clone https://github.com/Alexander86-N/python-project-52.git

cd python-project-52

make install
```
### Setting up Environment variables

Create a file in the root directory ".env" and prescribe in it:
- SECRET_KEY='something';
- DEBUG=True, if you want to enable debug mode;
- ACCESS_TOKEN='token_of_your_account_in_rollbar'.

### Running the application on a local server
```
make runserver
```
