#include "SensorRuido.hpp"
#include <random>

SensorRuido::SensorRuido() : SensorBase("ruido") {}

std::string SensorRuido::getTipo() const {
    return "ruido";
}

double SensorRuido::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        // 30–120 dB
        std::uniform_real_distribution<double> dist(30.0, 120.0);
        return dist(gen);
    } else {
        // fuera de rango alto 120–150 dB
        std::uniform_real_distribution<double> out(120.1, 150.0);
        return out(gen);
    }
}
