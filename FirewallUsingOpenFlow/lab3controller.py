# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    print "Example Code."
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    arp = packet.find('arp')
    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    ipv4 = packet.find('ipv4')
   
  

   # if ipv4 is None:
    #         return
     #   print "source ip:", ip.srcip

   
   
    
    if packet.find('icmp'):
      ip_packet = packet.payload
      src_ip = ip_packet.srcip
      dst_ip = ip_packet.dstip
      print(src_ip)
      print(dst_ip)
      print("enteredicmp")
      if (src_ip == '10.0.1.10' and  dst_ip  == '10.0.1.40'):  
            msg.data = packet_in
            print("icmpsent")
           
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
      elif (src_ip == '10.0.1.40' and  dst_ip  == '10.0.1.10'):
           msg.data = packet_in
           print("icmpsent")
           
           msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
           self.connection.send(msg)
      else:   
               return

    elif packet.find('arp'):
        if packet.find("ipv4"):
          return
        print("enteredarp")
        msg.data = packet_in
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)
    elif packet.find('tcp'):
    
        print("enteredtcp")
        msg.data = packet_in
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)
   
    else:
                 return
  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
