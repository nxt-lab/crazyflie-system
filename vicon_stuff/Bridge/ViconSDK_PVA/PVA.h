#ifndef PVA_H
#define PVA_H

#include "Drones.h"

typedef struct {
	Drones* drones;	
	unsigned int frame_number ;
	std::string object_name; // multiple objects
} PVA_DATA ;

#endif




