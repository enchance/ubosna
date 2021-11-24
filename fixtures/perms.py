


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

# Perm combinations:
# edit: ['read', 'update']
# make: ['create', 'delete',]
# attach: ['attach', 'detach']
# ban: ['ban', 'unban']
# close: ['close', 'reopen']

# All users have these groups
perm_init = {
    'AccountGroup': {
        'settings': ['edit'],
        'uploads': ['edit', 'make'],
        'options': ['edit']
        # 'taxo': ['manage'],
    },
    'TradeGroup': {
        'trade': ['make', 'edit'],
        # 'mark': ['manage'],
        # 'broker': ['read'] + attacher,
        # 'collection': cud + attacher,
    },
    # Users can only have one or none of a group ending in "-Set".
    # Normal users have neither of these.
    'ModGroupSet': {
        'settings': ['edit_mod'],
        'options': ['edit_mod'],
        # 'broker': ['edit'],
        # 'taxo': cud_mod + attacher_mod,
        'account': ['ban']
    }
}
perm_init['AdminGroupSet'] = {
    **perm_init['ModGroupSet'],
    # 'broker': cud + attacher_mod,
    'account': ['ban', 'close', 'create']
    
}

# ContentGroup = {
#     'owner': ['read'],
#     'equity': ['read'],
#
#     # Delete this soon so update wherever this was used
#     'content': crud
# }