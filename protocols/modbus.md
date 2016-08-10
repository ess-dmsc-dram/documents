# What is modbus

- Modbus is a communication protocol (see [wikipedia](https://en.wikipedia.org/wiki/Modbus))
- Master/slave architecture
- Request from master to slave has
    - Adress of slave
    - Function code
    - Data (payload, arguments to function call, max. 127 byte)
    - Checksum bits

- Slave device has
    - Coils:
        - 1 bit
        - read/write
        - 16 bit address
        - Associated function codes: 1 (read multiple coils), 5 (write single coils), 15 (write multiple coils)

    - Discrete inputs:
        - 1 bit
        - read
        - 16 bit address
        - Associated function codes: 2 (read multiple discrete inputs)

    - Holding registers:
        - 16 bit
        - read/write
        - 16 bit address
        - Associated function codes: 3 (read multiple registers), 6 (write single register), 16 (write multiple registers)

    - Input registers:
        - 16 bit
        - read
        - 16 bit address
        - Associated function codes: 4 (read multiple registers)

- Slave replies with response
    - Slave address
    - Function code
    - Data (max. 127 byte)
    
- Data types larger than 16 bit have to be distributed over multiple registers

# Modbus in Python

- Module [pymodbus](https://pymodbus.readthedocs.io)
- Function-codes described above are modeled as Request/Respone objects:

    request = SomeModbusRequest(...)
    response = modbus_client.execute(request)

- Can also function as a TCP server, useful for device simulators