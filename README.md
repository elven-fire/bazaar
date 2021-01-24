bazaar
======

An Elven Fire utility to automate the rolls necessary to sell items in town.

## Prerequisites

The bazaar requires access to the base elvenfire library. One simple way to accomplish this is to create a symbolic link to the library's location within the bazaar base directory. For example, if both repos are clones in the same directory:

```
ln -s ../elvenfire/elvenfire elvenfire
```

## Command-line interface

The bazaar contains a built-in wizard accessible from the command line to guide you through the decision of which method of selling is best for you. Simply launch the program, providing your character's IQ, and follow the prompts to sell your items.

```
python3 bazaar.py --IQ 14
```

Alternately, if you already know what method you wish to use and what item(s) you hope to sell, you can provide these details directly on the command line to streamline the responses.

```
python3 bazaar.py --IQ 12 --consignment --value 1000 1200
python3 bazaar.py --IQ 12 --private-market --value 1000 1200
```

If you have a modifier in effect (such as Create Artifact), you can note that on the command line to have bazaar automatically apply the modifier. The modifier given should be a percent value (e.g. --modifier 25 adds an additional 25% to the final offer price).

```
python3 bazaar.py -i 16 -cv 1000 --modifier 25
```
