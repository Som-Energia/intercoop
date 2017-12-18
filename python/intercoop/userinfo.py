# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os


class BadUser(Exception):
    def __init__(self, user):
        super(BadUser, self).__init__(
            "User not found '{}'".format(user))

class BadField(Exception):
    def __init__(self, field):
        super(BadField, self).__init__(
            "Unrecognized user field '{}'".format(field))

class UserInfo(object):
    """This mock object returns user info related to provided keys.
    In your system the substitute of this object should use the ERP
    to get such information.
    """

    def __init__(self, datadir):
        self.datadir = datadir

    def _userData(self, user):
        try:
            return ns.load(os.path.join(self.datadir, user+'.yaml'))
        except Exception:
            raise BadUser(user)

    def language(self, user):
        userdata = self._userData(user)
        try:
            return userdata.lang
        except AttributeError:
            return 'es'

    def getFields(self, user, fields):
        userdata = self._userData(user)

        for field in fields:
            if field not in userdata:
                raise BadField(field)

        return ns([
            (key, value)
            for key,value in userdata.items()
            if key in fields
            ])

    def fieldLabels(self, fields):
        userdata = ns.loads(labelsyaml)
        
        for field in fields:
            if field not in userdata:
                raise BadField(field)

        return ns([
            (key, value)
            for key,value in userdata.items()
            if key in fields
            ])

labelsyaml=u"""\
originpeer:
    es: Entidad de procedencia
    ca: Entitat de provinença
    en: Source entity
lang:
    es: Idioma preferente
    ca: Idioma preferent
    en: Preferred language
nif:
    es: NIF
    ca: NIF
    en: NIF
name:
    es: Nombre
    ca: Nom
    en: Name
peerroles:
    es: Roles
    ca: Rols
    en: Roles
innerid:
    es: Número de socio/a
    ca: Número de soci/a
    en: Member number
address:
    es: Dirección
    ca: Adreça
    en: Address
city:
    es: Municipio
    ca: Municipi
    en: City
state:
    es: Província
    ca: Provincia
    en: State
postalcode:
    es: Código postal
    ca: Codi postal
    en: Postal code
country:
    es: Nacionalidad
    ca: Nacionalitat
    en: Country
email:
    es: Correo electrónico
    ca: Correu electrònic
    en: e-mail
phone:
    es: Teléfono
    ca: Telèfon
    en: Phone
proxynif:
    es: NIF del representante
    ca: NIF del representant
    en: Proxy NIF
proxyname:
    es: Nombre del representante
    ca: Nom del representant
    en: Proxy name
"""



# vim: ts=4 sw=4 et
