#include "SensorPresion.hpp"
#include <random>

SensorPresion::SensorPresion() : SensorBase("presion") {}

std::string SensorPresion::getTipo() const {
    return "presion";
}

double SensorPresion::leerValor() const {
    static std::default_random_engine gen(std::random_device{}());
    std::uniform_int_distribution<int> chance(1,100);
    if (chance(gen) <= 90) {
        // 990–1025 hPa
        std::uniform_real_distribution<double> dist(990.0, 1025.0);
        return dist(gen);
    } else {
        // fuera de rango alto 1025–1040 hPa
        std::uniform_real_distribution<double> out(1025.1, 1040.0);
        return out(gen);
    }
}
