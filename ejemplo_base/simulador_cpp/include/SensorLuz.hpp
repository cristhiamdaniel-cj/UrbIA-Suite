#pragma once
#include "SensorBase.hpp"

class SensorLuz : public SensorBase {
public:
    SensorLuz();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
