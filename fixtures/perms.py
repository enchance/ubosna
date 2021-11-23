


cud =  ['create', 'update', 'delete']
cud_mod =  ['create_mod', 'update_mod', 'delete_mod']
attacher = ['attach', 'detach']
attacher_mod = ['attach_mod', 'detach_mod']
full =  [
    'create', 'read', 'update', 'delete', 'hard_delete',
    'attach', 'detach',
]
banning = ['ban', 'unban']
closing = ['close', 'reopen']

# All users have these groups
perm_init = {
    'AccountGroup': {
        'profile': ['read', 'update'],
        'settings': ['read', 'update'],
        'upload': cud,
        'message': cud,
        'taxo': cud,
    },
    'TradeGroup': {
        'trade': cud,
        'mark': cud,
        'broker': ['read'] + attacher,
        'collection': cud + attacher,
    },
    # Users can only have one or none of a group ending in "-Set".
    # Normal users have neither of these.
    'ModGroupSet': {
        'settings': ['read_mod', 'update_mod'],
        'broker': attacher_mod,
        'taxo': cud_mod + attacher_mod,
        'account': banning + closing,
    }
}
perm_init['AdminGroupSet'] = {
    **perm_init['ModGroupSet'],
    'broker': cud + attacher_mod,
    'account': ['create', 'delete'] + banning + closing,
    
}

# ContentGroup = {
#     'owner': ['read'],
#     'equity': ['read'],
#
#     # Delete this soon so update wherever this was used
#     'content': crud
# }