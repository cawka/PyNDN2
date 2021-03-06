# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# See COPYING for copyright and distribution information.
#

"""
This module defines the IdentityStorage abstract class which is a base class for
the storage of identity, public keys and certificates.  Private keys are stored
in PrivateKeyStorage. This is an abstract base class.  A subclass must implement
the methods.
"""

import math
from pyndn.util.common import Common
from pyndn.security.security_exception import SecurityException

class IdentityStorage(object):
    def doesIdentityExist(self, identityName):
        """
        Check if the specified identity already exists.

        :param Name identityName: The identity name.
        :return: True if the identity exists, otherwise False.
        :rtype: bool
        """
        raise RuntimeError("doesIdentityExist is not implemented")

    def addIdentity(self, identityName):
        """
        Add a new identity. An exception will be thrown if the identity already
        exists.

        :param Name identityName: The identity name.
        """
        raise RuntimeError("doesIdentityExist is not implemented")

    def revokeIdentity(self):
        """
        Revoke the identity.

        :return: True if the identity was revoked, False if not.
        :rtype: bool
        """
        raise RuntimeError("doesIdentityExist is not implemented")

    def getNewKeyName(self, identityName, useKsk):
        """
        Generate a name for a new key belonging to the identity.

        :param Name identityName: The identity name.
        :param bool useKsk: If True, generate a KSK name, otherwise a DSK name.
        :return: The generated key name.
        :rtype: Name
        """
        nowString = repr(math.floor(
          Common.getNowMilliseconds() / 1000.0)).replace(".0", "")
        if useKsk:
            keyIdStr = "KSK-" + nowString;
        else:
            keyIdStr = "DSK-" + nowString;

        keyName = Name(identityName).append(keyIdStr)

        if self.doesKeyExist(keyName):
            raise SecurityException("Key name already exists")

        return keyName

    def doesKeyExist(self, keyName):
        """
        Check if the specified key already exists.

        :param Name keyName: The name of the key.
        :return: True if the key exists, otherwise False.
        :rtype: bool
        """
        raise RuntimeError("doesKeyExist is not implemented")

    def addKey(self, keyName, keyType, publicKeyDer):
        """
        Add a public key to the identity storage.

        :param Name keyName: The name of the public key to be added.
        :param keyType: Type of the public key to be added.
        :type keyType: int from KeyType
        :param Blob publicKeyDer: A blob of the public key DER to be added.
        """
        raise RuntimeError("addKey is not implemented")

    def getKey(self, keyName):
        """
        Get the public key DER blob from the identity storage.

        :param Name keyName: The name of the requested public key.
        :return: The DER Blob. If not found, return a isNull() Blob.
        :rtype: Blob
        """
        raise RuntimeError("getKey is not implemented")

    def activateKey(self, keyName):
        """
        Activate a key. If a key is marked as inactive, its private part will
        not be used in packet signing.

        :param Name keyName: The name of the key.
        """
        raise RuntimeError("activateKey is not implemented")

    def deactivateKey(self, keyName):
        """
        Deactivate a key. If a key is marked as inactive, its private part will
        not be used in packet signing.

        :param Name keyName: The name of the key.
        """
        raise RuntimeError("deactivateKey is not implemented")

    def doesCertificateExist(self, certificateName):
        """
        Check if the specified certificate already exists.

        :param Name certificateName: The name of the certificate.
        :return: True if the certificate exists, otherwise False.
        :rtype: bool
        """
        raise RuntimeError("doesCertificateExist is not implemented")

    def addCertificate(self, certificate):
        """
        Add a certificate to the identity storage.

        :param IdentityCertificate certificate: The certificate to be added.
          This makes a copy of the certificate.
        """
        raise RuntimeError("addCertificate is not implemented")

    def getCertificate(self, certificateName, allowAny = False):
        """
        Get a certificate from the identity storage.

        :param Name certificateName: The name of the requested certificate.
        :param bool allowAny: (optional) If False, only a valid certificate will
          be returned, otherwise validity is disregarded.  If omitted,
          allowAny is False.
        :return: The requested certificate. If not found, return None.
        :rtype: Data
        """
        raise RuntimeError("getCertificate is not implemented")

    #
    # Get/Set Default
    #

    def getDefaultIdentity(self):
        """
        Get the default identity.

        :return: The name of default identity, or an empty name if there is no
          default.
        :rtype: Name
        """
        raise RuntimeError("getDefaultIdentity is not implemented")

    def getDefaultKeyNameForIdentity(self, identityName):
        """
        Get the default key name for the specified identity.

        :param Name identityName: The identity name.
        :return: The default key name.
        :rtype: Name
        """
        raise RuntimeError("getDefaultKeyNameForIdentity is not implemented")

    def getDefaultCertificateNameForIdentity(self, identityName):
        """
        Get the default certificate name for the specified identity.

        :param Name identityName: The identity name.
        :return: The default certificate name.
        :rtype: Name
        """
        keyName = self.getDefaultKeyNameForIdentity(identityName)
        return getDefaultCertificateNameForKey(keyName)

    def getDefaultCertificateNameForKey(self, keyName):
        """
        Get the default certificate name for the specified key.

        :param Name keyName: The key name.
        :return: The default certificate name.
        :rtype: Name
        """
        raise RuntimeError("getDefaultCertificateNameForKey is not implemented")

    def setDefaultIdentity(self, identityName):
        """
        Set the default identity. If the identityName does not exist, then clear
        the default identity so that getDefaultIdentity() returns an empty name.

        :param Name identityName: The default identity name.
        """
        raise RuntimeError("setDefaultIdentity is not implemented")

    def setDefaultKeyNameForIdentity(self, keyName, identityNameCheck = None):
        """
        Set the default key name for the specified identity.


        :param Name keyName: The key name.
        :param Name identityNameCheck: (optional) The identity name to check the
          keyName.
        """
        raise RuntimeError("setDefaultKeyNameForIdentity is not implemented")

    def setDefaultCertificateNameForKey(self, keyName, certificateName):
        """
        Set the default key name for the specified identity.

        :param Name keyName: The key name.
        :param Name certificateName: The certificate name.
        """
        raise RuntimeError("setDefaultCertificateNameForKey is not implemented")
