#!/bin/bash

spark-submit \
    --master local[*] \
    /app/drift_detector.py