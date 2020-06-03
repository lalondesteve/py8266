#!/usr/bin/env bash

for i in *.py; do
  ampy put "$i";
done

for i in *.html; do
  ampy put "$i";
done

for i in *.conf; do
  ampy put "$i";
done

