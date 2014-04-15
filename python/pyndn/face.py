# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# See COPYING for copyright and distribution information.
#

"""
This module defines the Face class which provides the main methods for NDN
communication.
"""

from pyndn.interest import Interest
from pyndn.forwarding_flags import ForwardingFlags
from pyndn.encoding.wire_format import WireFormat
from pyndn.transport.tcp_transport import TcpTransport
from pyndn.node import Node

class Face(object):
    """
    Create a new Face for communication with an NDN hub.  This constructor
    has the forms Face(transport, connectionInfo) or
    Face(host, port)

    :param Transport transport: An object of a subclass of Transport used for
      communication.
    :param Transport.ConnectionInfo connectionInfo: An object of a subclass of
      Transport.ConnectionInfo to be used to connect to the transport.
    :param str host: In the Face(host, port) form of the constructor, host is
      the host of the NDN hub with a TcpTransport.
    :param int port: (optional) In the Face(host, port) form of the constructor,
      port is the port of the NDN hub. If omitted. use 6363.
    """
    def __init__(self, arg1, arg2 = None):
        if type(arg1) is str:
            transport = TcpTransport()
            connectionInfo = TcpTransport.ConnectionInfo(
              arg1, arg2 if type(arg2) is int else 6363)
        else:
            transport = arg1
            connectionInfo = arg2

        self._node = Node(transport, connectionInfo)

    def expressInterest(
      self, interestOrName, arg2, arg3 = None, arg4 = None, arg5 = None):
        """
        Send the Interest through the transport, read the entire response and
        call onData(interest, data).  There are two forms of expressInterest.
        The first form takes the exact interest (including lifetime):
        expressInterest(interest, onData [, onTimeout] [, wireFormat]).
        The second form creates the interest from a name and optional
        interest template:
        expressInterest(name [, interestTemplate], onData [, onTimeout]
        [, wireFormat]).

        :param Interest interest: The Interest (if the first form is used). This
          copies the Interest.
        :param Name name: A name for the Interest (if the second form is used).
        :param Interest interestTemplate: (optional) if not None, copy interest
          selectors from the template (if the second form is used).  If omitted,
          use a default interest lifetime.
        :param onData: A function object to call when a matching data packet is
          received.
        :type onData: function object
        :param onTimeout: (optional) A function object to call if the interest
          times out. If onTimeout is None or omitted, this does not use it.
        :type onTimeout: function object
        :param wireFormat: (optional) A WireFormat object used to encode the
           message. If omitted, use WireFormat.getDefaultWireFormat().
        :type wireFormat: A subclass of WireFormat
        :return:  The pending interest ID which can be used with
          removePendingInterest.
        :rtype: int
        """
        # expressInterest(interest, onData)
        # expressInterest(interest, onData, wireFormat)
        # expressInterest(interest, onData, onTimeout)
        # expressInterest(interest, onData, onTimeout, wireFormat)
        if type(interestOrName) is Interest:
            # Node.expressInterest requires a copy of the interest.
            interest = Interest(interestOrName)
            onData = arg2
            if isinstance(arg3, WireFormat):
                onTimeout = None
                wireFormat = arg3
            else:
                onTimeout = arg3
                wireFormat = arg4
        else:
            # The first argument is a name. Make the interest from the name and
            #   possible template.
            interest = Interest(interestOrName)

            # expressInterest(name, interestTemplate, onData)
            # expressInterest(name, interestTemplate, onData, wireFormat)
            # expressInterest(name, interestTemplate, onData, onTimeout)
            # expressInterest(name, interestTemplate, onData, onTimeout, wireFormat)
            if type(arg2) is Interest:
                template = arg2
                interest.setMinSuffixComponents(template.getMinSuffixComponents())
                interest.setMaxSuffixComponents(template.getMaxSuffixComponents())
                interest.setKeyLocator(template.getKeyLocator())
                interest.setExclude(template.getExclude())
                interest.setChildSelector(template.getChildSelector())
                interest.setMustBeFresh(template.getMustBeFresh())
                interest.setScope(template.getScope())
                interest.setInterestLifetimeMilliseconds(
                  template.getInterestLifetimeMilliseconds())
                # Don't copy the nonce.

                onData = arg3
                if isinstance(arg4, WireFormat):
                    onTimeout = None
                    wireFormat = arg4
                else:
                    onTimeout = arg4
                    wireFormat = arg5
            # expressInterest(name, onData)
            # expressInterest(name, onData, wireFormat)
            # expressInterest(name, onData, onTimeout)
            # expressInterest(name, onData, onTimeout, wireFormat)
            else:
                # Set a default interest lifetime.
                interest.setInterestLifetimeMilliseconds(4000.0)
                onData = arg2
                if isinstance(arg3, WireFormat):
                    onTimeout = None
                    wireFormat = arg3
                else:
                    onTimeout = arg3
                    wireFormat = arg4

        if wireFormat == None:
            # Don't use a default argument since getDefaultWireFormat can change.
            wireFormat = WireFormat.getDefaultWireFormat()

        return self._node.expressInterest(
          interest, onData, onTimeout, wireFormat)

    def removePendingInterest(self, pendingInterestId):
        """
        Remove the pending interest entry with the pendingInterestId from the
        pending interest table. This does not affect another pending interest
        with a different pendingInterestId, even if it has the same interest
        name. If there is no entry with the pendingInterestId, do nothing.

        :param int pendingInterestId: The ID returned from expressInterest.
        """
        self._node.removePendingInterest(pendingInterestId)

    def registerPrefix(
      self, prefix, onInterest, onRegisterFailed, flags = None,
      wireFormat = None):
        """
        Register prefix with the connected NDN hub and call onInterest when a
        matching interest is received.

        :param Name prefix: The Name for the prefix to register which is NOT
          copied for this internal Node method. The Face registerPrefix is
          reponsible for making a copy for Node to use..
        :param onInterest: A function object to call when a matching interest is
          received.
        :type onInterest: function object
        :param onRegisterFailed: A function object to call if failed to retrieve
          the connected hub's ID or failed to register the prefix.
        :type onRegisterFailed: function object
        :param ForwardingFlags flags: The flags for finer control of which
          interests are forwardedto the application.
        :param wireFormat: A WireFormat object used to encode the message.
        :type wireFormat: a subclass of WireFormat
        """
        if flags == None:
            flags = ForwardingFlags()
        if wireFormat == None:
            # Don't use a default argument since getDefaultWireFormat can change.
            wireFormat = WireFormat.getDefaultWireFormat()

        # Node.expressInterest requires a copy of the prefix.
        self._node.registerPrefix(
          prefix, onInterest, onRegisterFailed, flags, wireFormat)

    def removeRegisteredPrefix(self, registeredPrefixId):
        """
        Remove the registered prefix entry with the registeredPrefixId from the
        registered prefix table. This does not affect another registered prefix
        with a different registeredPrefixId, even if it has the same prefix
        name. If there is no entry with the registeredPrefixId, do nothing.

        :param int registeredPrefixId: The ID returned from registerPrefix.
        """
        self._node.removeRegisteredPrefix(registeredPrefixId)

    def processEvents(self):
        """
        Process any packets to receive and call callbacks such as onData,
        onInterest or onTimeout. This returns immediately if there is no data to
        receive. This blocks while calling the callbacks. You should repeatedly
        call this from an event loop, with calls to sleep as needed so that the
        loop doesn't use 100% of the CPU. Since processEvents modifies the pending
        interest table, your application should make sure that it calls
        processEvents in the same thread as expressInterest (which also modifies
        the pending interest table).

        :raises: This may raise an exception for reading data or in the callback
          for processing the data.  If you call this from an main event loop,
          you may want to catch and log/disregard all exceptions.
        """
        # Just call Node's processEvents.
        self._node.processEvents()

    def shutdown(self):
        """
        Shut down and disconnect this Face.
        """
        self._node.shutdown()
