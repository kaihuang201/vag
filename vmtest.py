import libvirt

conn = libvirt.open('qemu:///system')
names = conn.listDefinedDomains()

if __name__=='__main__':
    print names
