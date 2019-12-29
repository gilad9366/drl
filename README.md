
CONTENTS OF THIS FILE
---------------------

 * Instructions
 * Introduction
 * How to run

INSTRUCTIONS
------------
Distributed Rate Limiter

Implement a rate limiting API for a globally distributed load balancer (say, deployed at 5 AWS regions)

A given user will be recognized by a user ID string that the load balancers will provide as a request parameter.

Each user is allowed to perform up to 500 requests in a 60 seconds time frame.

Notes:

Requests from a given user are not guaranteed to always end up at the same AWS region

The rate limiting functionality must be as fast as possible since it's a blocking call made by the Load Balancer during the user's request/response cycle

Do think about: RPC protocol, networking concerns regarding service latency, Latency vs accuracy of response

No need to provide a running system - code & basic instructions on how to run it locally is enough :)

INTRODUCTION
------------

Distrubuted Rate Limiter

By: Gilad Sever

This application runs a containerized distributed rate limiter using redis.


HOW TO RUN
----------

git clone the project

docker-compose up --build

