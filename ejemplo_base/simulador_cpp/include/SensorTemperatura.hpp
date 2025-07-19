#pragma once
#include "SensorBase.hpp"

class SensorTemperatura : public SensorBase {
public:
    SensorTemperatura();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
