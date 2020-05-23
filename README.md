# preapp
a tool to help both users and developers create a software project. 

## Goals
this tool is still very early in developement. the end goal is for users (people with little or no programming experience) to be able to select features and requirements they have for a app or piece of software then have preap automatically generate the project files and github repositories for them. they can then use the github platform to look for developers to work on their project. 

## Usage
preapp is a cli tool it supports both predefined and terminal input.

run preapp with user cli input

```$ python -m preapp ```

run preapp with predefined json input

```$ python -m preapp --preset config.json --credentials credentials.json```

## Current State
currently preapp can create primitive repositories from some project specifications. 

## Contributing
want to help with preapp start [here](CONTRIBUTING.md)
