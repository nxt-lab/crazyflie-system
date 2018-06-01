#ifndef DRONE_H
#define DRONE_H

//**********************************************************//
//ENTER YOUR DRONES YOU WANT TO SEND THE VICON DATA TO HERE//
class Drones
{
	public:
		 std::string name;			 //eg quad
		 PCSTR IP;					//eg "192.168.2.51"
		// std::string IP;
		 SOCKET ConnectSocket;
		 float position[3] ;		//x,y,z
		 float orientation[3] ;	//z,y,z
};

#endif