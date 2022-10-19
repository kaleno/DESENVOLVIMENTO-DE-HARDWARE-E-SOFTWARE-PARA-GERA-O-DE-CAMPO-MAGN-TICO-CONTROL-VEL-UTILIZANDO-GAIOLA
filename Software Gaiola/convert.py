import pygpib as gpib

interface = gpib.list_adapters()[0]

interface.open(primary_address=10)

instrument = interface.get_instrument(primary_address=22)
instrument.configure(end_read_on_eos=True, eos_char='\n')

instrument.query('*IDN?')
