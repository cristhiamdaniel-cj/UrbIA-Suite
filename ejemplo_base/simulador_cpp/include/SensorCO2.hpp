#pragma once
#include "SensorBase.hpp"

class SensorCO2 : public SensorBase {
public:
    SensorCO2();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
