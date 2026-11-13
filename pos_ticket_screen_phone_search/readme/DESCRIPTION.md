Adds a *Phone* option to the search of the PoS *Orders* screen, so orders can
be found by the phone of their customer, both among active orders and among
paid orders searched on the server.

Among active orders the search is fuzzy, like the other options: the typed
digits only need to appear in the same order, so spaces do not matter, but
extra orders may show up. Among paid orders the server looks for the exact
text, so a phone saved with spaces must be searched with the same spaces.
