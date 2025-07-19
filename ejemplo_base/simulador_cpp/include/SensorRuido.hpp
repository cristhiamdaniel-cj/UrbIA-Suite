#pragma once
#include "SensorBase.hpp"

class SensorRuido : public SensorBase {
public:
    SensorRuido();
    std::string getTipo() const override;    // Declaración de la función
    double leerValor() const override;       // Declaración de la función
};
