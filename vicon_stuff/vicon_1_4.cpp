// Basic readout of DataStreamSDK
//V1.4
// Go then...
#include "DataStreamClient.h"

#include <iostream>
#include <cassert>
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include <limits>
#include <math.h>
#include <string>

#ifdef WIN32
  #include <conio.h>   // For _kbhit()
  #include <cstdio>   // For getchar()
  #include <windows.h> // For Sleep()
#else
  #include <unistd.h> // For sleep()
#endif // WIN32

#include <time.h>

using namespace ViconDataStreamSDK::CPP;

#define output_stream if(!LogFile.empty()) ; else std::cout

namespace //Magic setup?
{
  std::string Adapt( const bool i_Value )
  {
    return i_Value ? "True" : "False";
  }

  std::string Adapt( const Direction::Enum i_Direction )
  {
    switch( i_Direction )
    {
      case Direction::Forward:
        return "Forward";
      case Direction::Backward:
        return "Backward";
      case Direction::Left:
        return "Left";
      case Direction::Right:
        return "Right";
      case Direction::Up:
        return "Up";
      case Direction::Down:
        return "Down";
      default:
        return "Unknown";
    }
  }

  std::string Adapt( const DeviceType::Enum i_DeviceType )
  {
    switch( i_DeviceType )
    {
      case DeviceType::ForcePlate:
        return "ForcePlate";
      case DeviceType::Unknown:
      default:
        return "Unknown";
    }
  }

  std::string Adapt( const Unit::Enum i_Unit )
  {
    switch( i_Unit )
    {
      case Unit::Meter:
        return "Meter";
      case Unit::Volt:
        return "Volt";
      case Unit::NewtonMeter:
        return "NewtonMeter";
      case Unit::Newton:
        return "Newton";
      case Unit::Unknown:
      default:
        return "Unknown";
    }
  }
}

int main(int argc, char* argv[]) {

  // Make new client
  Client MyClient;

    std::string HostIP = "localhost:801"; //[-] Fillin
  //[^] std::string HostIP = "224.0.0.0:801"
    std::string MultiIP = "224.0.0.1:801"


  while( !MyClient.IsConnected().Connected )
    {
      // Direct connection
      MyClient.Connect( HostIP );

      // Multicast connection
      /MyClient.ConnectToMulticast( HostIP, MultiIP );

      std::cout << ".";

    }
    std::cout << std::endl;

  bool TransmitMulticast = false; //we are connecting not trasmitting

  if( TransmitMulticast )
  {
    MyClient.StartTransmittingMulticast();
  }

  // Set the streaming mode
  MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ClientPull );
  //[^] MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ClientPullPreFetch );
  //[^] MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ServerPush );

  // Set the global up axis
  MyClient.SetAxisMapping( Direction::Forward,
                           Direction::Left,
                           Direction::Up ); // Z-up

  //[x] previously commented out
  MyClient.SetGlobalUpAxis(Direction::Forward,
                           Direction::Up,
                           Direction::Right ); // Y-up

  Output_GetAxisMapping _Output_GetAxisMapping = MyClient.GetAxisMapping();
  std::cout << "Axis Mapping: X-" << Adapt( _Output_GetAxisMapping.XAxis )
                         << " Y-" << Adapt( _Output_GetAxisMapping.YAxis )
                         << " Z-" << Adapt( _Output_GetAxisMapping.ZAxis ) << std::endl;


  // Get subject name
  std::string SubjectName = MyClient.GetSubjectName( 0 ).SubjectName;
  std::cout << "            Name: " << SubjectName << std::endl;


  //get number of markers
  unsigned int MarkerCount = MyClient.GetMarkerCount( SubjectName ).MarkerCount;
  std::cout << "    Markers (" << MarkerCount << "):" << std::endl;
  for( unsigned int MarkerIndex = 0 ; MarkerIndex < MarkerCount ; ++MarkerIndex )
  {
    // Get marker name
    std::string MarkerName = MyClient.GetMarkerName( SubjectName, MarkerIndex ).MarkerName;
  }

  if( TransmitMulticast )
  {
    MyClient.StopTransmittingMulticast();
  }

   MyClient.Disconnect();

} // ...there are other worlds than these.
