# This file is part party_vat_unique module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.


from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Party', 'PartyIdentifier']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    @classmethod
    def copy(cls, parties, default=None):
        if default is None:
            default = {}
        default['identifiers'] = None
        return super(Party, cls).copy(parties, default=default)


class PartyIdentifier(metaclass=PoolMeta):
    __name__ = 'party.identifier'

    @classmethod
    def validate(cls, identifiers):
        super(PartyIdentifier, cls).validate(identifiers)
        for identifier in identifiers:
            identifier.unique_code()

    def unique_code(self):
        # Warn on existing code and type
        user = Transaction().user

        if self.id > 0 and user > 1:
            identifiers = Pool().get('party.identifier')
            identifiers_count = identifiers.search_count([('code', '=', self.code), ('type', '=', 'eu_vat')])
            if identifiers_count > 1:
                self.raise_user_warning(
                    'warn_identifier_with_same_code.%d' % self.id,
                    'There is another code with the same number: %s',
                    self.rec_name,
                )
