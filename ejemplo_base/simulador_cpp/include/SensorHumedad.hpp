#pragma once
#include "SensorBase.hpp"

class SensorHumedad : public SensorBase {
public:
    SensorHumedad();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
