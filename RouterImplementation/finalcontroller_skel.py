# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    print "Hello, World!"
    


    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
  
    tcp = packet.find('tcp')
    arp = packet.find('arp')
    icmp = packet.find('icmp')
    if packet.find('arp'):
         print("arp")
         msg = of.ofp_flow_mod()
         msg.idle_timoeut = 30
         msg.hard_timeout = 30
         
         msg.match = of.ofp_match.from_packet(packet)
         msg.buffer_id = packet_in.buffer_id
         msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  
         self.connection.send(msg)
    elif packet.find('icmp'):
        print("icmp")
        ip_packet =  packet.payload
        src_ip = ip_packet.srcip
        dst_ip = ip_packet.dstip
        print(src_ip)
        print(dst_ip)
            
        if (src_ip == '10.0.1.101' and dst_ip  == '10.0.2.102'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.1.101' and dst_ip  == '10.0.3.103'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.1.101' and dst_ip  == '10.0.4.104'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.2.102' and  dst_ip  == '10.0.1.101'):
            print("srv2")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.2.102' and  dst_ip  == '10.0.3.103'):
            print("srv2")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.2.102' and  dst_ip  == '10.0.4.104'):
             print("srv2")
             msg.data = packet_in
             msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
             self.connection.send(msg)
        if (src_ip == '10.0.3.103' and  dst_ip  == '10.0.1.101'):
             print("srv3")
             msg.data = packet_in
             msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
             self.connection.send(msg)
        if (src_ip == '10.0.3.103' and  dst_ip  == '10.0.2.102'):
             print("srv3")
             msg.data = packet_in
             msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
             self.connection.send(msg)
        if (src_ip == '10.0.3.103' and  dst_ip  == '10.0.4.104'):
             print("srv3")
             msg.data = packet_in
             msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
             self.connection.send(msg)
        if (src_ip == '10.0.4.104' and dst_ip  == '10.0.1.101'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.4.104' and dst_ip  == '10.0.3.103'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '10.0.4.104' and dst_ip  == '10.0.2.102'):  
            print("srv1")
            msg.data = packet_in
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
        if (src_ip == '128.114.50.10' or dst_ip  == '128.114.50.10'):
             print("untrust")
           
        else:
             return
    if packet.find('tcp'):
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
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
