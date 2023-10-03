<!-- markdownlint-disable MD041 MD013 -->

META_START
web_title Enid's Blog | My Homelab

og:title My Homelab
og:image TODO

description Welcome to my homelab!
author Enid
META_END

# My Homelab

Welcome to my homelab! In this article I will outline the equipment I use and how I do so. This article is split into multiple parts for easy finding. I will add images of my homelab later on.

The total cost of my homelab as of TODO is TODO.

## Parts

1. [Networking](#networking)
2. [Servers](#servers)
3. [Software](#software)

## Networking

1. [Software-side networking setup](#software-side-networking-setup)
2. [UniFi Dream Router](#unifi-dream-router)
3. [TP-Link TL-WA801N](#tp-link-tl-wa801n)
4. [MikroTik CRS326-24G-2S+RM](#mikrotik-crs326-24g-2srm)
5. [TP-Link RE700X](#tp-link-re700x)

### Software-side networking setup

As my networking setup is probably of a bigger scale than one might expect I deem it worthy of its own point.

I currently have eight subnets and five WiFi Networks. These are separated by concern and have according firewall and isolation rules in place (WiFi in parenthesis after the name indicates having an associated SSID):

1. Trusted Devices, 10.1.0.0/24 (WiFi): The network for my day-to-day trusted devices.
2. Non-essential Devices, 10.1.1.0/24 (WiFi): The network for my day-to-day non-essential devices. These don't have full network access and are separated for easier housekeeping.
3. Untrusted Devices: 10.1.2.0/24 (WiFi): This network is primarily used for IoT devices and others that I may not fully trust. Clients are isolated and are only allowed to phone home for updates.
4. Guests, 10.1.3.0/24 (WiFI): This network, as the name implies, is for guests who visit me. It also has client isolation, no LAN access but offers full WAN access.
5. Wireguard: 10.1.4.0/24, This network isn't in use but my router but moreso exists as a placeholder to avoid accidentally using reserved IP spaces. As the wireguard server that handles traffic is part of the virtual server network it has full access to the network as with my trusted devices network.
6. Physical Servers, 10.2.0.0/24: This network is reserved for my physical servers and shares rules with my trusted devices and virtual servers.
7. Virtual Servers, 10.2.1.0/24: See above.
8. Proxmox Internal, 10.3.0.0/24: This is another reserved IP space for Proxmox inter-node software-defined networking. It has no access outside of servers and nothing can access it directly either.

All of these have their own VLAN and a network for networking devices/management interfaces exist at VLAN 0 (10.0.0.0/24).

### UniFi Dream Router

The core of my network is a UniFi Dream Router. The choice on it fell as I wanted WiFi 6 supportas well as a portable machine that's hackable but also provides easy web management capabilities. Originally I wanted to go for a custom router with pfsense but due to monetary constraints at the time I chose against that. However, it does remain a plan for the future.

At 230.23€ it was definitely definitely a tough pill to swallow at the time but a well worth it one. Due to being a Ubiquiti product is integrates nicely into their system which offers an Apple-like ecosystem if you want to go that route in the future. Performance is astounding and it handles my rather overkill usecase with ease. One of the only downsides is that all WiFi SSIDs share a single channel, which is why I decided to invest in an access point (see next entry).

Another issue I had was that BIOS/UEFI network booting in unison is not natively possible. The workaround was a quick find with some googling but it requires manually changing Dnsmasq configurations on the device directly which get overwritten with every software update.

### TP-Link TL-WA801N

This was quite the interesting one. I got a gift card for a local technology store from my workplace for Christmas 2022 and needed an access point as my router only supports one band for all networks. As I have quite a few wireless networks I was running into issues with overcongestion so I used it for this AP.

It was quite cheap at 21.99€ and does a great job. While it only offers 100mbps as its maximum that's more than plenty for my needs as I only use it to broadcast networks used by my Raspberry Pi and smart outlets.

It also offers SNMP and VLAN support which is absolutely amazing at that pricepoint.

### MikroTik CRS326-24G-2S+RM

This is probably the device I actively use the most in my homelab. It's a rather affordable (210.68€) switch for what it offers and I don't regret buying it at all. While my homelab has already outgrown its 10gbps capabilities it is still a decent consideration if you want a fully managed switch with two SFP+ ports for a reasonable price.

Other than that there's not a lot to say about it. It offers everything you except from a more enterprise-oriented switch. Rackmountability? Completely managed system? VLANs? You name it. It also has a serial port which is something I've been wanting to get into at the time to gain experience. It also runs RouterOS (optionally SwitchOS) with hardware offloading for up to one networking bridge.

At the time that I got it the two SFP+ ports sufficed for my needs (only two servers capable of it). By now I've sadly outgrown that but it will remain in my homelab for all my gigabit ethernet needs.

### TP-Link RE700X

This access point is the latest addition to my homelab and is probably the least interesting. It cost me around 60€ and is a rather basic extender-style access point. It meshes with my main WiFi network to offer coverage all around the house and supports WiFi 6 at up to 3gbps. I got it primarily since it sits nicely underneath the light switches in our living room.

## Servers

1. [HP ProDesk 600 G1 SFF](#hp-prodesk-600-g1-sff)
2. [Intel NUC 9 Extreme](#intel-nuc-9-extreme)
3. [IBM x3650 M4](#ibm-x3650-m4)
4. [Raspberry Pi 4 4GB](#raspberry-pi-4-4gb)

### HP ProDesk 600 G1 SFF

The first PC I got which I am using as a server. I got it for around 54.99€ with an i3-4160 and 8GB of RAM. As for storage I originally added an old SSD (250GB) and HDD (2TB) that I had laying around. By now I've upgraded it to an i7-4770k with 32GB of RAM and a 2TB SSD.

Here's the specs for easy readability:

- Form Factor: Small Form Factor
- CPU: i7-4770k
- GPU: Intel HD 4600
- RAM: Crucial 32GB DDR3-1600
- Storage: Crucial MX500 2TB
- Additional Cards:
  - Mellanox Connect-X 2 single port 10gbps NIC

### Intel NUC 9 Extreme

After the ProDesk I wanted a second node for redundancy and wanted it to be portable. I went for a NUC as it fits both of those criteria. The Extreme variant also offers two PCIe slots (which run at a max of PCIe 3 x4 speeds in my configuration). As for storage I am using a Samsung 970 EVO Plus with 2TB of storage as well as a 1TB one. As for RAM I added 64GB of Corsair Vengeance DDR4L-2666. I paid 436.00€ for the NUC and 195.50€ for the RAM.

The specs again in list format:

- Form Factor: Mini PC (somewhere between normal NUC size and SFF)
- CPU: i7-9750H
- GPU: Intel UHD 620
- RAM: Corsair Vengeance 64GB DDR4L-2666
- Storage: Samsung 970 EVO Plus 2TB
- Additional Cards:
  - Generic PCIe x4 to NVMe adapter with another 960 EVO Plus (1TB)

### IBM x3650 M4

This is the latest addition to my homelab and the deal I'm the proudest of. I paid 229.00€ for a full 2U server including dual Xeon E5-2650V2s, 128GB of DDR3-1600 ECC memory and blank trays for the 24 2.5" slots it offers. For storage I added a 2TB Crucial MX500 and for 10gbps connectivity a Mellanox Connect-X 2.

I bought this server more because I had to than by choice. I originally planned on upgrading the TrueNAS instance on my NUC to 4x 2TB NVMe. However, I didn't realize that the NUC doesn't support bifurcation in the way needed and a card with a PCIe switch to make this project possible would've been around the same price as this server. As it has 6 PCIe 3 x8 slots I still have one left!

Specs:

- Form Factor: 19" Server, 2U
- CPUs: 2x Xeon E5-2650V2
- GPU: None
- RAM: Unknown Brand 128GB DDR3-1600 ECC
- Storage: Crucial MX500 2TB
- Additional Cards:
  - Mellanox Connect-X 2 single port 10gbps NIC
  - 4x Generic PCIe x4 to NVMe adapter each with a Crucial P3 2TB NVMe

### Raspberry Pi 4 4GB

This is a simple one. It's a Raspberry Pi 4 with 4GB of RAM that runs Home Assistant for all my smart home needs. It runs it bare-metal and has a Sonoff ZigBee USB for my ZigBee-enabled devices.

## Software

Now we gotta talk about software! What do I do with all this hardware? How do I put it into use?

As for OS all my servers run the latest version of Proxmox VE community edition on which I have virtual machines for dedicated tasks. These tasks include:

- DNS (Redundant)
- Reverse Proxy
- Wireguard
- Plex
- TrueNAS
- etc.

Furthermore, I do host and intend to host other resource intensive things (like game servers for local debugging, my own GitLab instance for private projects, etc.). As it stands right now my most used self-hosted services are Plex and my NAS which runs TrueNAS Scale with four NVMe drives in RAIDZ1 (added via PCIe forwarding) and offers a total capacity of around 5TiB usable space. I do intend to, later on, upgrade this to at least 24TB, potentially more.
