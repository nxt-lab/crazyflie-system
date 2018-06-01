
#include "stdafx.h"
#include "comms.h"
#include "serial_comms.h"
#include "pva.h"

// Need to link with Ws2_32.lib, Mswsock.lib, and Advapi32.lib
#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

#define DEFAULT_BUFLEN 512
#define DEFAULT_PORT "7901"
#define HEADER_CHAR 0x55
#define COMMAND_CODE_DATA_STATE 0x20

extern PVA_DATA pva;
extern int number_of_drones;

void send_PVA_data(void)
{
  int i ;
  unsigned char checksum=0 ;
  char packet[255] ;
  static unsigned int index=1000;
  static unsigned char cmd_code=0;

  /*------SET TO FINAL PACKET WHEN CHANGING PACKET------------*/
	int finalpacketnum = 3+24; //Where 24 is the packet size so 4*3 for the position + 4*3 for the orientation || 3 is the offset from header
   /*------SET TO FINAL PACKET WHEN CHANGING PACKET------------*/

  packet[0] = HEADER_CHAR ;
  packet[1] = cmd_code++; //COMMAND_CODE_DATA_STATE ;
  packet[2] = finalpacketnum ; ////
  
  for(int index=0; index < number_of_drones; index++ )
   {
	   int multiplier = 3; //current drone * packet size for that drone + initial header offset
	   stofloat(pva.drones[index].position[0], packet+multiplier) ;
	   stofloat(pva.drones[index].position[1], packet+4+multiplier) ;
	   stofloat(pva.drones[index].position[2], packet+8+multiplier) ;
	   
	   stofloat(pva.drones[index].orientation[0], packet+12+multiplier) ;
	   stofloat(pva.drones[index].orientation[1], packet+16+multiplier) ;
	   stofloat(pva.drones[index].orientation[2], packet+20+multiplier) ;
	   stouint(pva.frame_number, packet+finalpacketnum) ;

	   for (i=1; i<finalpacketnum ; i++)//// 
		checksum += ((unsigned char) packet[i]) ;

	  packet[finalpacketnum] = checksum ;////
	  send(pva.drones[index].ConnectSocket, packet, finalpacketnum+1, 0 ); ////
	  std::cout<<"packet"<<" :  " << pva.drones[index].ConnectSocket<<std::endl;
  }  
}

int init_socket(void)
{
 for(int index=0; index < number_of_drones; index++ )
   {
	WSADATA wsaData;
    pva.drones[index].ConnectSocket = INVALID_SOCKET;
    struct addrinfo *result = NULL,
                    *ptr = NULL,
                    hints;
    int iResult;

   // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (iResult != 0) {
        printf("WSAStartup failed with error: %d\n", iResult);
        return 1;
    }

    ZeroMemory( &hints, sizeof(hints) );
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM ; //SOCK_STREAM;
    hints.ai_protocol = IPPROTO_UDP ; //IPPROTO_TCP;

	printf("Get the server address and port\n") ;
    //Sleep(2000) ;

     //Resolve the server address and port
    iResult = getaddrinfo(pva.drones[index].IP, DEFAULT_PORT, &hints, &result); // or 192.168.1.2 ***********************************
	//iResult = getaddrinfo("192.168.0.104", DEFAULT_PORT, &hints, &result); 

    if ( iResult != 0 ) {
        printf("getaddrinfo failed with error: %d\n", iResult);
        WSACleanup();
		Sleep(1000) ;
        return 1;
    }
	printf("Attempt to connect to an address\n") ;
	//Sleep(2000) ;
    // Attempt to connect to an address until one succeeds
    for(ptr=result; ptr != NULL ;ptr=ptr->ai_next) {

        // Create a SOCKET for connecting to server
        pva.drones[index].ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype, 
            ptr->ai_protocol);
        if (pva.drones[index].ConnectSocket == INVALID_SOCKET) {
            printf("socket failed with error: %ld\n", WSAGetLastError());
            WSACleanup();
			Sleep(2000) ;
            return 1;
        }
		printf("Connect to server\n") ;
		//Sleep(1000); 
        // Connect to server.
        iResult = connect(pva.drones[index].ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (iResult == SOCKET_ERROR) {
			printf("Socket Error\n") ;
			Sleep(2000) ;
            closesocket(pva.drones[index].ConnectSocket);
            pva.drones[index].ConnectSocket = INVALID_SOCKET;
            continue;
        }
        break;
    }

    freeaddrinfo(result);

    if (pva.drones[index].ConnectSocket == INVALID_SOCKET) {
        printf("Unable to connect to server!\n");
        WSACleanup();
		Sleep(2000) ;
        return 1;
    }
 }

	return 0 ;
}

void close_socket(void)
{
	for(int index=0; index < number_of_drones; index++ )
   {
  // cleanup
   closesocket(pva.drones[index].ConnectSocket);
    WSACleanup();
	}
}


void stoshort(short n, char *s)
{
    s[0] = (char) (n>>8) ;
    s[1] = (char) (n&0xFF) ;
}

void stoushort(unsigned short n, char* s)
{
    s[0] = (char) (n>>8) ;
    s[1] = (char) (n&0xFF) ;
}

void stouint(unsigned int n, char *s)
{
	char *temp ;
	
	temp = (char *) &n ;
	s[0] = temp[0] ;
	s[1] = temp[1] ;
	s[2] = temp[2] ;
	s[3] = temp[3] ;
}

void stouint_reverse(unsigned int n, char *s)
{
	char *temp ;
	
	temp = (char *) &n ;
	s[3] = temp[0] ;
	s[2] = temp[1] ;
	s[1] = temp[2] ;
	s[0] = temp[3] ;
}

void stoint(int n, char *s)
{
	char *temp ;
	
	temp = (char *) &n ;
	s[0] = temp[0] ;
	s[1] = temp[1] ;
	s[2] = temp[2] ;
	s[3] = temp[3] ;
}

void stolong(long long int n, char *s)
{
  char *temp ; int i;
	
  temp = (char *) &n ;
  for (i=0;i<8;i++) s[i] = temp[i] ;
}

void stodouble(double n, char *s)
{
  char *temp ; int i;
	
  temp = (char *) &n ;
  for (i=0;i<8;i++) s[i] = temp[i] ;
}

void stofloat(float n, char *s)
{
  char *temp ; int i;

  temp = (char *) &n ;
  for (i=0; i<4; i++) s[i] = temp[i] ;
}

