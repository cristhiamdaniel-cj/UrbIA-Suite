#pragma once
#include "SensorBase.hpp"

class SensorPresion : public SensorBase {
public:
    SensorPresion();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
