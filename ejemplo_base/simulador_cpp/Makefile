# Makefile para compilar el simulador de sensores en UrbIA

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude

SRC_DIR = src
BUILD_DIR = build
TARGET = sensor_simulator

SOURCES = \
	$(SRC_DIR)/main.cpp \
	$(SRC_DIR)/SensorCO2.cpp \
	$(SRC_DIR)/SensorTemperatura.cpp \
	$(SRC_DIR)/SensorHumedad.cpp \
	$(SRC_DIR)/SensorPresion.cpp \
	$(SRC_DIR)/SensorLuz.cpp \
	$(SRC_DIR)/SensorRuido.cpp \
	$(SRC_DIR)/HttpClient.cpp \
	$(SRC_DIR)/EnvLoader.cpp \
	$(SRC_DIR)/Logger.cpp

OBJECTS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SOURCES))

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $@ -lcurl

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

run: all
	./$(TARGET)

clean:
	rm -rf $(BUILD_DIR) $(TARGET)
