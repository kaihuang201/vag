Install KVM libvirt and setup access (the following commands are for Red Hat, for other distros it may be a little different)
- sudo yum install kvm virt-manager libvirt libvirt-python python-virtinst libvirt-bin
 sudo yum groupinstall "Virtualization Hypervisor" "Virtualization Client"

- To restart libvirtd, run one of the following:
    service libvirtd restart
    /etc/init.d/libvirt restart

- To grant a user access, add the user to the group named libvirt
    sudo usermod -G libvirt -a <username>

- To test whether a user has access to libvirt, use the following python snippet. It should return a valid conn object.

    import libvirt
    conn = libvirt.open('qemu:///system')

From here on, you can start setting up and using the autograder...

http://libvirt.org/goals.html
http://wiki.libvirt.org/page/VM_lifecycle

The basic idea is to use domains for testing students' code.

- Define and start the testing domain(s)
- Take a clean-slate snapshot as soon as the domain is up and running
- For each students in the queue:
    - Uploaded and grade a student's code, and send results back to the autograder running on the node
    - Restore the domain to the clean-slate snapshot
