#pragma once
#include <string>

class SensorBase {
protected:
    std::string nombre;

public:
    SensorBase(const std::string& nombre) : nombre(nombre) {}
    virtual ~SensorBase() = default;

    virtual std::string getTipo() const = 0;
    virtual double leerValor() const = 0;

    std::string getNombre() const {
        return nombre;
    }
};
