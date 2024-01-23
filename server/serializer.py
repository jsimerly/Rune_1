from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user.user import User
    from team.team import Team
    from game.game import Game

def serialize_user(user: User):
    return {
        'username': user.username
    }

def serialize_team(team: Team):
    return {
        'user': serialize_user(team.user),
        'team_id': team.team_id,
        'characters': team.characters
    }

def serializer_draft_start(draft):
    return {
        'draft_id': draft.draft_id,
        'team_1': serialize_team(draft.team_1),
        'team_2': serialize_team(draft.team_2)
    }

def serializer_game_start(game: Game):
    return {
        'game_id': game.game_id,
        'team_1': serialize_team(game.team_1),
        'team_2': serialize_team(game.team_2),
        'round': game.round
    }

def serializer_draft_ban(user: User, character):
    return {
        'type': 'drafting',
        'user': serialize_user(user),
        'character': character,
        'pick_ban': 'ban'
    }

def serializer_draft_pick(user: User, character):
    return {
        'type': 'drafting',
        'user': serialize_user(user),
        'character': character,
        'pick_ban': 'pick'
    }

