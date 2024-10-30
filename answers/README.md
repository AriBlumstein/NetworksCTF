## Stage 1 - Wireshark, HTTP cookies, SCAPY, PE format
Let us start by view the .pcapng file in wireshark to view the packets captured. We see the following:
![wireshark picture](../resources/wireshark.png)
In the back story we were told to focus on certain types of packets, here we can see that Ariel seemed to have been interested in ARP, DHCP and ICMP packets. Wireshark gives the ability to filter for certain packets within a capture, so let us do just that.

First we look at the ARP packets. ARP (Address Resolution Protocol) is a layer 2 protocol whose purpose is to find the MAC address of the device that has a certain IP address, as generally the requesting device and the requested device appear one the same local network. When we filter for ARP we see thousands of such packets. Wireshark gives us the ability to view the layers of a packet and when we do so with one of the filtered packets, we see the following:
![ARP packet](../resources/ARP.png)
We see a broadcast ARP packet, where the sending device sent the packet to every other device on the local network using the broadcast MAC address, trying to find out the IP address of a specific device. There's nothing particularly out of the ordinary here, however, wireshark gives us the ability to view the packets as raw bytes, and here we can see there seems to have been a secret payload attached to the packet when it was sent:

![ARP Payload](../resources/ARP_payload.png)

**ARP is not what you should you be filtering for, would you say that ‘The-Supermarket’ might be some sort of unique header?**

Now let's look at the DHCP packets. DHCP (Dynamic Host Configuration Protocol) is a layer 5 protocol, whose purpose is get an IP address for a device that just connected to a local network. When we filter for these packets we see again many DHCP discover requests, as many devices seem to be looking for the DHCP server to recieve and IP address for the network. Let us again view the layers of one of these packets and see if there are any secrets. We will notice, that there seems to be a secret in the *vendor class indetifier option* which generally indicates the hardware being used to help the DHCP server decide on configuration:
![DHCP secret](../resources/DHCP_vendor.png)

Finally let us look at the ICMP packets. ICMP (Internet Control Message Protocol) is a layer 3 protocol who's purpose is for error reporting and network diagnostics. When we filter for these packets, we see ICMP echo requests, where devices ask other devices to echo back the packet. So, this might indicate to us to check the payload to see what was the echo request:
![ICMP echo](../resources/ICMP_echo.png)

**ICMP is not what you should be filtering for, what type of snack is an oreo?**

We finally now see what we should be filtering for: HTTP packets that contain the unique header field 'The-Supermarket', and we should focus on the cookies header.


