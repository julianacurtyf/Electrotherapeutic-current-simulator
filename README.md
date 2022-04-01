# Electrotherapy

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/julianacurtyf/Electrotherapy.git
$ cd Electrotherapy
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Walkthrough

Once you runned the server, you will get to a home page:


![image](https://user-images.githubusercontent.com/93845875/161304823-51c1a90c-1780-4623-be74-b427f492fcda.png)


In this page you can choose the current that you want to simulate, this tutorial will be done with 'Corrente ITP'. 


![image](https://user-images.githubusercontent.com/93845875/161305203-3ba51204-342b-4366-a180-b0c759af1d86.png)


After choosing that current, you will be redirectionated to the page above, where we have a simple description of the current and the parameters to be defined. The range of each parameter is already described, since we are dealing with different frequencies and units to simulate a real case, if you put different values, the program may not work properly. You can see below an example of this wave selected.


![image](https://user-images.githubusercontent.com/93845875/161306097-0fb4a486-f7ed-47c4-be62-71e496c79c09.png)


## Technologies

The project was developed mainly using Django (Python), aswell as html, css and javascript for the website template. For the graph, we used a javascript library named d3.js (https://d3js.org/d3.v7.min.js).
