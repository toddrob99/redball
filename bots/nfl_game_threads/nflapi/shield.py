import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


shield = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
shield -= sgqlc.types.relay.Node
shield -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
class AuthorOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'displayName', 'person__displayName')


class BigInteger(sgqlc.types.Scalar):
    __schema__ = shield


Boolean = sgqlc.types.Boolean

class CheerleaderOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'cheerleaderPerson__displayName', 'person__displayName', 'season__season')


class ClipType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PREVIEW', 'GAME_HIGHLIGHT', 'IN_GAME_HIGHLIGHT', 'FANTASY_HIGHLIGHT', 'CLUB_TV', 'FEATURE', 'LOCKER_ROOM_SOUND', 'PRESS_CONFERENCE', 'DIARIES', 'HIGHLIGHT_REEL', 'INTERVIEWS', 'NFL_NOW', 'PLAYER_HIGHLIGHT', 'RECAP', 'SHOW', 'TEAM_HIGHLIGHT', 'FANTASY_PLAYERRECAP', 'LIVE_CONTENT_CORRESPONDENTS')


class CoachOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'coachPerson__displayName', 'person__displayName', 'season__season')


class CoachType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('HEAD_COACH', 'UNASSIGNED')


class Conference(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('AFC', 'NFC', 'NFL_EAST', 'NFL_WEST', 'AFL_EAST', 'AFL_WEST', 'EASTERN_CONFERENCE', 'WESTERN_CONFERENCE', 'AMERICAN_CONFERENCE', 'AMERICAN_FOOTBALL_CONFERENCE', 'NATIONAL_CONFERENCE', 'NATIONAL_FOOTBALL_CONFERENCE', 'EASTERN_DIVISION', 'WESTERN_DIVISION', 'NFL_EASTERN_DIVISION', 'NFL_WESTERN_DIVISION', 'NFL_EASTERN_CONFERENCE', 'NFL_WESTERN_CONFERENCE', 'AFL_EASTERN_DIVISION', 'AFL_EASTERN_CONFERENCE', 'AFL_WESTERN_DIVISION', 'AFL_WESTERN_CONFERENCE', 'AAFC_EASTERN_DIVISION', 'AAFC_WESTERN_DIVISION', 'NO_CONFERENCE', 'HISTORICAL')


class ContentHint(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ARTICLE', 'AUDIO', 'IMAGE', 'PHOTO', 'VIDEO', 'EVENT', 'PROMO', 'CONTENT_LIST', 'MIXED')


class ContentOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'originalPublishDate', 'lastPublishDate')


class ContentType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('VIDEO', 'AUDIO', 'EVENT', 'PROMO', 'IMAGE', 'ARTICLE', 'CONTENTLIST', 'PERSONLIST')


class Curation(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('DYNAMIC', 'EDITORIAL', 'META', 'TAG')


class CurrentContext(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('DEFAULT', 'GAME', 'COMBINE', 'DRAFT', 'PLAYER', 'CHEERLEADER', 'COACH', 'EXECUTIVE', 'STANDINGS', 'STATS', 'TEAM')


class CurrentType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('SEASON', 'SEASON_TYPE', 'WEEK')


Date = sgqlc.types.datetime.Date

DateTime = sgqlc.types.datetime.DateTime

class DayOfWeek(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY')


class DisplayHint(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('SHOW', 'DONT_SHOW')


class Division(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('AFC_NORTH', 'AFC_SOUTH', 'AFC_EAST', 'AFC_WEST', 'NFC_NORTH', 'NFC_SOUTH', 'NFC_EAST', 'NFC_WEST', 'AFC_CENTRAL', 'AFC_EASTERN', 'AFC_WESTERN', 'NFC_CENTRAL', 'NFC_EASTERN', 'NFC_WESTERN', 'CENTRAL', 'COASTAL', 'CAPITOL', 'CENTURY', 'HISTORICAL_DIVISION', 'NO_DIVISION')


class DraftPickOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'draftRound', 'draftNumberOverall')


class DraftState(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PRE', 'ACTIVE', 'IN', 'POST')


class EliasStatsLeadersOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('gamesPlayed', 'gamesStarted', 'gamesSub', 'gamesDnp', 'gamesInactive', 'passingAttempts', 'passingCompletions', 'passingYards', 'passingLong', 'passingLgtd', 'passingTouchdowns', 'passingFirstDowns', 'passingInterceptions', 'passingSacked', 'passingSackedYardsLost', 'passingNetYards', 'passingFumbles', 'passing20plusYardsEach', 'passing40plusYardsEach', 'passingPasserRating', 'passingCompletionPercentage', 'passingTouchdownPercentage', 'passingInterceptionPercentage', 'passingFirstDownPercentage', 'passingAverageYards', 'rushingAttempts', 'rushingYards', 'rushingLong', 'rushingLgtd', 'rushingTouchdowns', 'rushingFirstDowns', 'rushingFumbles', 'rushing20plusYardsEach', 'rushing40plusYardsEach', 'rushingAverageYards', 'rushingFirstDownPercentage', 'receivingReceptions', 'receivingYards', 'receivingLong', 'receivingLgtd', 'receivingTouchdowns', 'receivingFirstDowns', 'receivingFumbles', 'receivingTarget', 'receiving20plusYardsEach', 'receiving40plusYardsEach', 'receivingAverageYards', 'receivingFirstDownPercentage', 'defensiveInterceptions', 'defensiveInterceptionsYards', 'defensiveInterceptionsLong', 'defensiveInterceptionsLgtd', 'defensiveInterceptionsTds', 'defensiveInterceptionsAvgyds', 'puntReturns', 'puntReturnsYards', 'puntReturnsLong', 'puntReturnsLgtd', 'puntReturnsTouchdowns', 'puntReturnsFumbles', 'puntReturnsFairCatches', 'puntReturnsAverageYards', 'puntReturns20plusYardsEach', 'puntReturns40plusYardsEach', 'kickReturns', 'kickReturnsYards', 'kickReturnsLong', 'kickReturnsLgtd', 'kickReturnsTouchdowns', 'kickReturnsFumbles', 'kickReturnsFairCatches', 'kickReturnsAverageYards', 'kickReturns20plusYardsEach', 'kickReturns40plusYardsEach', 'puntingPunts', 'puntingYards', 'puntingLong', 'puntingAverageYards', 'puntingBlocked', 'puntingPuntsInside20', 'puntingTotalPuntsInclBlks', 'puntingTouchbacks', 'puntingDowned', 'puntingOutOfBounds', 'puntingPuntsFairCaught', 'puntingNumberReturned', 'puntingReturnYards', 'puntingReturnTouchdowns', 'puntingNetYardage', 'kickoffTotal', 'kickoffYards', 'kickoffAverageYards', 'kickoffTouchbacks', 'kickoffTouchbacksPercentage', 'kickoffReturns', 'kickoffReturnsYards', 'kickoffReturnsAverageYards', 'kickoffReturnsTouchdowns', 'kickoffOnside', 'kickoffOnsideRecovered', 'kickoffOutbounds', 'kickoffFairCaught', 'kickingFgMade', 'kickingFgAtt', 'kickingFgBlk', 'kickingFgLong', 'kickingFgPct', 'kickingXkMade', 'kickingXkAtt', 'kickingXkBlk', 'kickingXkPct', 'kickingFgAttMade1To19', 'kickingFgAttMade20To29', 'kickingFgAttMade30To39', 'kickingFgAttMade40To49', 'kickingFgAttMade50plus', 'totalPointsScored', 'touchdownsTotal', 'touchdownsRushing', 'touchdownsReceiving', 'touchdownsPassing', 'touchdownsInterceptionRtrns', 'touchdownsPuntReturns', 'touchdownsKickReturns', 'touchdownsFumbleReturns', 'touchdownsBlockedFgReturns', 'touchdownsBlockedPuntRtrns', 'touchdownsMissedFgReturns', 'touchdownsKoRecInEndzone', 'touchdownsOffLateralHist', 'defensiveSafeties', 'extraPointGood2ptNonkick', 'extraPointAtt2ptNonkick', 'defensiveTotalTackles', 'defensiveSoloTackles', 'defensiveCombineTackles', 'defensiveAssists', 'defensiveSacks', 'defensivePassesDefensed', 'defensiveForcedFumble', 'defensivePuntBlocked', 'defensiveFgBlocked', 'defensiveXpBlocked', 'defensiveAllKickBlocked', 'fumblesTotal', 'fumblesLost', 'fumblesOutbounds', 'fumblesTouchback', 'fumblesSafety', 'fumblesAbortedYds', 'teammateFumbleRecovery', 'teammateFumbleYds', 'teammateFumbleLong', 'teammateFumbleLgtd', 'teammateFumbleTd', 'opponentFumbleRecovery', 'opponentFumbleYds', 'opponentFumbleLong', 'opponentFumbleLgtd', 'opponentFumbleTd', 'firstdownsTotal', 'firstdownsRush', 'firstdownsPass', 'firstdownsPenalty', 'down1stFdMade', 'down1stAttempted', 'down2ndFdMade', 'down2ndAttempted', 'down3rdFdMade', 'down3rdAttempted', 'down4thFdMade', 'down4thAttempted', 'scrimmagePlays', 'scrimmageYds', 'timeOfPossSeconds', 'penaltiesTotal', 'penaltiesYardsPenalized', 'recordWins', 'recordLosses', 'recordTies', 'recordWinPct', 'startPosition', 'touchdownsOffense', 'touchdownsDefense', 'pointsPerGameAverage', 'yardsPerGameAverage', 'timeOfPossSecondsPerGameAverage', 'turnoverDifferential', 'totalPointsScoredPerGameAverage', 'firstDownsPerGameAverage')


class Entitlement(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('FREE', 'PREMIUM', 'HIDDEN')


class EventType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('LIVE', 'REPLAY')


class ExecutiveOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'executivePerson__displayName', 'person__displayName', 'season__season')


class Existence(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('NOT_NULL', 'NULL')


Float = sgqlc.types.Float

class ForPurchase(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('BUY_NOW', 'NOT_AVAILABLE')


class FranchiseOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'name')


class FranchiseState(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ACTIVE', 'INACTIVE')


class GameOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('week__seasonValue', 'week__weekValue', 'week__weekOrder', 'week__weekType', 'gameTime')


ID = sgqlc.types.ID

class IdpFilterType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ENABLED', 'DISABLED', 'ALL')


class ImageType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('VIDEO_IMAGE', 'VIDEO_ASSET_POSTER_IMAGE', 'VIDEO_COLLECTION_IMAGE', 'PHOTO_GALLERY_IMAGE', 'MISC')


class InjuryReportOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'team_abbreviation', 'week__seasonValue', 'week__weekValue', 'week__weekOrder', 'week__weekType')


class InjuryStatus(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('NOT_LISTED', 'QUESTIONABLE', 'PROBABLE', 'DOUBTFUL', 'OUT')


class InsightTemplate(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('GAMES_LIST_TEASER', 'RESEARCH_FACT', 'PLAYER_FEATURE', 'TEAM_FEATURE', 'PLAYER_COMPARISON', 'TEAM_COMPARISON', 'PLAYER_TEAM_COMPARISON', 'RANKING', 'PLAYOFF_IMPLICATIONS')


Int = sgqlc.types.Int

class ItemPicker(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('TEAM', 'PLAYER')


class League(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('AAC', 'AFL', 'NFL')


class LegacyId(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('SEASON', 'SEASON_TYPE', 'WEEK', 'YEAR', 'GAME_ID', 'SITE_ID', 'GSIS_GAME_KEY', 'DRIVE_SEQ', 'PLAY_ID', 'PLAY_STAT_ID', 'PLAY_STAT_SEQ', 'GAME_INSIGHT_SEQ', 'PERSON_ESB_ID', 'PERSON_GSIS_ID', 'PERSON_ALFRESCO', 'PERSON_NFL_ID', 'PERSON_GLOBAL', 'PERSON_TYPE', 'TEAM_ID', 'TEAM_SEQ', 'DRAFT_SEQ', 'OFFICIAL_TRANSACTION', 'NDC_ALFRESCO', 'CLUB_ARTICLE', 'CLUB_AUDIO', 'CLUB_VIDEO', 'FORGE_ARTICLE', 'FORGE_AUDIO', 'FORGE_EVENT', 'FORGE_PROMO', 'FORGE_VIDEO', 'FORGE_IMAGE', 'FORGE_DOCUMENT', 'FORGE_CONTENT_LIST', 'FORGE_PERSON_LIST', 'FORGE_CLUB_ROSTER', 'FORGE_SERIES', 'NDC_VIDEO_CHANNEL', 'NDC_VIDEO_CHANNEL_CATEGORY', 'NDC_RANKING', 'NDC_DYNAMIC_TITLE_RANKING', 'NDC_VIDEO_CHANNEL_CATEGORIES', 'NDC_ALFRESCO_EVENT', 'NDC_ALFRESCO_SHOW', 'NDC_ALFRESCO_CATEGORY', 'NDC_PROGRAM', 'NDC_PARTNER', 'TEAM_STAT_TYPE', 'CLUB_NOW_VIDEO_ASSET', 'CLUB_NOW_VIDEO', 'CLUB_TEAMSITE_EVENT', 'CLUB_DRUPAL_EVENT', 'CONTENT_PROVIDER', 'SHIELD_SCREEN', 'SHIELD_BROADCAST', 'NL_VIDEO', 'NL_AUDIO', 'BROCHURE', 'BROCHURE_SHARED_DATA', 'AUDIO_ASSET', 'VIDEO_ASSET_VODZILLA', 'VIDEO_ASSET_ALFRESCO', 'VIDEO_ASSET_DRUPAL', 'VIDEO_ASSET_TEAMSITE', 'POCKET_VIDEO_VODZILLA', 'POCKET_VIDEO_TEAMSITE', 'POCKET_VIDEO_DRUPAL', 'POCKET_VIDEO_ALFRESCO', 'PROPERTY', 'EVENT', 'SHOW', 'MUSIC', 'MUSIC_LIBRARY', 'EPISODE', 'IMAGE_ASSET_VODZILLA', 'IMAGE_ASSET_ALFRESCO', 'IMAGE_ASSET_DRUPAL', 'IMAGE_ASSET_TEAMSITE', 'POCKET_IMAGE_VODZILLA', 'POCKET_IMAGE_TEAMSITE', 'POCKET_IMAGE_DRUPAL', 'POCKET_IMAGE_ALFRESCO', 'PUSH_DB_NOTIFICATION', 'BREAKING_NEWS', 'DCL_AUDIO_ASSET', 'DCL_VIDEO_ASSET', 'CLOUDINARY_IMAGE_ASSET', 'STREAM_GUYS_AUDIO_ASSET', 'TAG', 'DATE', 'GSIS_PLAYER_NAME', 'MCP_ID', 'ADOBEPASS_MSO_ID', 'IDENTITY_PROVIDER_GROUP', 'AUTH_PROVIDER', 'NETWORK', 'CALL_SIGN', 'TMS_ID', 'MCP_DIGITAL_SHOW_TYPE', 'VERSION', 'AUTHOR', 'ENDPOINT_KEY', 'SLUG', 'SMART_ID')


class LiveGameRosterStatus(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PLAYER_SUBSTITUTE', 'ACTIVE_DID_NOT_PLAY', 'INJURED_DID_NOT_PLAY', 'NOT_ACTIVE', 'INJURED_RESERVE', 'STARTED')


class Long(sgqlc.types.Scalar):
    __schema__ = shield


class Map(sgqlc.types.Scalar):
    __schema__ = shield


class MaterializationHint(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('CHANNEL', 'RANKING', 'CATEGORY')


class MilestoneType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PASSING_YARDS', 'RECEIVING_YARDS', 'RUSHING_YARDS', 'PASSING_TD', 'RECEIVING_TD', 'RUSHING_TD', 'SACKS', 'FG_LONG', 'RECEPTIONS', 'COMBINED_TACKLES', 'RUSHING_TD_LONG', 'RECEIVING_TD_LONG', 'TOTAL_FG_MADE', 'RETURN_TD', 'INTERCEPTIONS', 'TEAM_SACKS', 'TEAM_TOTAL_OFFENSE', 'TEAM_PUNTS_BLOCKED', 'TEAM_TAKEAWAYS', 'TEAM_TOTAL_FIRST_DOWNS', 'TEAM_PENALTY_YARDS')


class MockDraftOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'year', 'version')


class MockDraftPickOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'pickNumber')


class NameOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'name')


class OrderByDates(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate')


class OrderByDirection(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('DESC', 'ASC')


class Origination(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('EXTERNAL_LIVE', 'EXTERNAL_VOD')


class PersonOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'displayName', 'lastName')


class Phase(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PREGAME', 'INGAME', 'HALFTIME', 'SUSPENDED', 'FINAL', 'FINAL_OVERTIME')


class Platoon(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('OFFENSE', 'DEFENSE', 'SPECIAL_TEAMS')


class PlayReviewStatus(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('NOT_REVIEWED', 'UNDER_REVIEW', 'REVIEWED', 'REVIEWED_OVERTURNED')


class PlayType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('GAME_START', 'TIMEOUT', 'FAIR_CATCH_KICK', 'FREE_KICK', 'END_QUARTER', 'COMMENT', 'END_GAME', 'PUNT', 'FIELD_GOAL', 'KICK_OFF', 'XP_KICK', 'PASS', 'SACK', 'RUSH', 'PENALTY', 'PAT2', 'PLAY_FROM_SCRIMMAGE')


class PlayerAwardsOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'person__firstName', 'person__lastName', 'person__displayName')


class PlayerOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'person__lastName', 'season__season')


class PlayerStatsLeadersOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('totalPointsScored', 'passingNetYards', 'rushingYards', 'receivingYards', 'firstdownsTotal', 'passingYards', 'touchdownsTotal', 'defensiveTotalTackles', 'defensiveAssists', 'defensiveSacks', 'defensiveInterceptions', 'kickingFgMade', 'puntingYards', 'kickReturns', 'totalTackles')


class Position(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('BB', 'C', 'CB', 'DB', 'DE', 'DG', 'DL', 'DT', 'E', 'EDGE', 'FB', 'FL', 'FS', 'G', 'H', 'HB', 'ILB', 'K', 'KOR', 'KR', 'LB', 'LS', 'MLB', 'NB', 'NG', 'NT', 'OE', 'OG', 'OL', 'OLB', 'OT', 'P', 'PK', 'PR', 'QB', 'RB', 'SAF', 'SS', 'S', 'T', 'TB', 'TE', 'WB', 'WR')


class PositionGroup(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ARB', 'CB', 'DB', 'DL', 'EDGE', 'HC', 'LB', 'OL', 'QB', 'RB', 'SPEC', 'TE', 'WR')


class ProfileType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('AUTHOR', 'CHEERLEADER', 'COACH', 'OFFICIAL', 'PLAYER', 'PROSPECT')


class PropertyOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'displayName', 'fullName')


class PropertyType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('POCKET', 'PARTNER')


class ProspectOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'person__displayName', 'year')


class PublishState(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PUBLISHED', 'UNPUBLISHED', 'UNLISTED')


class Recurrence(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('WEEKLY', 'BIWEEKLY', 'TRIWEEKLY', 'MONTHLY')


class Repository(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('POCKET', 'ENDZONE')


class ScoringPlayType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('TD', 'FG', 'PAT', 'PAT2', 'SFTY')


class SearchOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('CREATED_DATE', 'LAST_MODIFIED_DATE', 'LAST_PUBLISH_DATE', 'ORIGINAL_PUBLISH_DATE')


class SeasonOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('season',)


class SeasonType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('PRE', 'REG', 'POST', 'PRO')


class SeasonTypeOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('seasonType', 'season_season')


class SeriesType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('CATEGORY', 'AUDIO_CHANNEL', 'VIDEO_CHANNEL')


class SmartID(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('SEASON', 'WEEK', 'GAME', 'GAME_DETAIL', 'DRIVE', 'PLAY', 'TEAM', 'FRANCHISE', 'STANDING', 'STANDINGS', 'INJURY_REPORT', 'DEPTH_CHART', 'CURRENT', 'SITE', 'VENUE', 'PLAYER_TEAM', 'PERSON_TEAM', 'PERSON_GSISID', 'PERSON_GSISID_UNKNOWN', 'PERSON_NFLID', 'PERSON_ALFRESCO', 'PERSON_ESBID', 'PROSPECT_ESBID', 'COACH_PERSON_ESBID', 'PLAYER_ESBID', 'COACH_ESBID', 'PERSON', 'AUTHOR_PERSON', 'CHEERLEADER_PERSON', 'COACH_PERSON', 'EXECUTIVE_PERSON', 'OWNER_PERSON', 'AUTHOR', 'CHEERLEADER', 'COACH', 'EXECUTIVE', 'PROSPECT', 'PROSPECT_NFLID', 'DRAFT_PICK', 'DRAFT_TEAM', 'OFFICIAL_TRANSACTION', 'CLUB_TRANSACTION', 'PLAY_STAT', 'TEAM_GAME_STAT', 'TEAM_SEASON_STAT', 'PLAYER_GAME_STAT_GSIS', 'PROSPECT_COMBINE_STAT', 'PLAYER_TEAM_STAT', 'PLAYER_GAME_STAT', 'PLAYER_GAME_STAT_V3', 'PLAYER_STAT_V3', 'TEAM_GAME_STAT_V3', 'TEAM_STAT_V3', 'DCL_AUDIO_ASSET', 'DCL_VIDEO_ASSET', 'NDC_HEADSHOT_IMAGE', 'NDC_HEADSHOT_IMAGE_ASSET', 'CLOUDINARY_IMAGE_ASSET', 'STREAM_GUYS_AUDIO_ASSET', 'FORGE_ARTICLE', 'FORGE_AUDIO', 'FORGE_EVENT', 'FORGE_IMAGE', 'FORGE_PROMO', 'FORGE_VIDEO', 'FORGE_CONTENT_LIST', 'FORGE_PERSON_LIST', 'FORGE_CLUB_ROSTER', 'NDC_ALFRESCO_ARTICLE', 'CLUB_ARTICLE', 'NDC_ALFRESCO_VIDEO', 'POCKET_VIDEO', 'POCKET_VIDEO_VODZILLA', 'POCKET_VIDEO_TEAMSITE', 'POCKET_VIDEO_DRUPAL', 'POCKET_VIDEO_ALFRESCO', 'CLUB_VIDEO', 'CLUB_NOW_VIDEO', 'NL_VIDEO', 'POCKET_VIDEO_ASSET', 'CLUB_NOW_VIDEO_ASSET', 'VIDEO_ASSET_ALFRESCO', 'VIDEO_ASSET_VODZILLA', 'VIDEO_ASSET_TEAMSITE', 'VIDEO_ASSET_DRUPAL', 'NDC_ALFRESCO_EXTERNAL_LINK', 'NDC_VIDEO_CHANNEL', 'NDC_VIDEO_CHANNEL_CATEGORY', 'NDC_RANKING', 'NDC_RANKING_PAGE', 'NDC_VIDEO_CHANNEL_CATEGORIES', 'SHIELD_BROADCAST', 'NDC_DYNAMIC_TITLE_RANKING', 'NL_AUDIO', 'CLUB_AUDIO', 'AUDIO_ASSET', 'MUSIC', 'MUSIC_LIBRARY', 'IMAGE', 'POCKET_IMAGE_TEAMSITE', 'POCKET_IMAGE_DRUPAL', 'POCKET_IMAGE_ALFRESCO', 'IMAGE_ASSET', 'IMAGE_ASSET_TEAMSITE', 'IMAGE_ASSET_DRUPAL', 'IMAGE_ASSET_ALFRESCO', 'NDC_ALFRESCO_PHOTO_GALLERY', 'NDC_ALFRESCO_PHOTO_ESSAY', 'NDC_ALFRESCO_PHOTO', 'NDC_PARTNER', 'CONTENT_PROVIDER', 'PROPERTY', 'SHIELD_SCREEN', 'BROCHURE', 'BROCHURE_SHARED_DATA', 'NDC_ALFRESCO_EVENT', 'CLUB_TEAMSITE_EVENT', 'CLUB_DRUPAL_EVENT', 'ZEPPELIN_EVENT', 'DRAFT', 'COMBINE', 'NDC_ALFRESCO_SHOW', 'ZEPPELIN_SHOW', 'NDC_ALFRESCO_CATEGORY', 'NDC_PROGRAM', 'BREAKING_NEWS', 'TAG_CONTENT_LIST', 'POCKET_CONTENT_LIST', 'TAG', 'SERIES', 'PUSH_NOTIFICATION', 'TICKET_LOG', 'MEDIA_OBJECT', 'IDENTITY_PROVIDER', 'IDENTITY_PROVIDER_GROUP', 'AUTH_PROVIDER', 'NETWORK', 'CALL_SIGN', 'PROMOTION', 'BLACKLIST', 'GEO_CALL_SIGN', 'MOCK_DRAFT', 'MOCK_DRAFT_PICK', 'PERSON_LIST', 'MCP_SHOW', 'GAME_INSIGHT', 'CONTENT_TRAY', 'MCP_DIGITAL_SHOW', 'MCP_VOD')


class SplitCategory(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('Attempts', 'Days', 'Downs', 'Field_Position', 'Game_Halves', 'Home_vs_Road', 'Margin_of_Victory', 'Months', 'Opponents_by_Group', 'Opponents_by_Team', 'Outcomes', 'Point_Differential', 'Quarters', 'Season_Type', 'Stadium_Surfaces', 'Stadiums', 'Weather')


class StatsRole(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('TM', 'OPP')


class Status(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ACT', 'RET', 'NWT', 'TRL', 'TRC', 'TRD', 'TRT', 'RES', 'NON', 'RSN', 'INA', 'EXE', 'CUT', 'SUS', 'DEV', 'PUP', 'UFA', 'RFA', 'UDF', 'RSR', 'ANI', 'ANJ', 'DTR', 'DNR', 'DOL', 'DUS', 'EXR', 'FRR', 'FPL', 'FUT', 'IDR', 'IRC', 'MIL', 'NOS', 'RNI', 'COM', 'TRN', 'VFA', 'DIN', 'ERF', 'WAV')


String = sgqlc.types.String

class TeamOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'fullName', 'nickName', 'abbreviation')


class TeamStatsLeaderOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('offenseScrimmageYds', 'offenseScrimmageYdsPerGame', 'offensePassingNetYards', 'offensePassingNetYardsPerGame', 'offenseRushingYards', 'offenseRushingYardsPerGame', 'defenseScrimmageYds', 'defenseScrimmageYdsPerGame', 'defensePassingNetYards', 'defensePassingNetYardsPerGame', 'defenseRushingYards', 'defenseRushingYardsPerGame', 'totalTackles', 'defensiveTotalTackles', 'defensiveAssists', 'defensiveSacks', 'defensiveInterceptions')


class TeamType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('TEAM', 'PRO', 'AS')


class TransactionOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('createdDate', 'lastModifiedDate', 'transactionYear')


class Transition(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('INTERCEPTION', 'FUMBLE', 'PUNT', 'DOWNS', 'KICKOFF', 'SAFETY_KICK', 'TOUCHDOWN', 'FIELD_GOAL', 'SAFETY', 'END_HALF', 'END_GAME', 'OWN_KICKOFF', 'MUFFED_PUNT', 'MUFFED_KICKOFF', 'ONSIDE_KICK', 'MISSED_FG', 'FUMBLE_SAFETY', 'BLOCKED_PUNT', 'BLOCKED_PUNT_DOWNS', 'BLOCKED_FG', 'BLOCKED_FG_DOWNS')


class WeekOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('week__seasonValue', 'week__weekValue', 'week__weekOrder', 'week__weekType')


class WeekType(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('HOF', 'PRE', 'REG', 'WC', 'DIV', 'CONF', 'SB', 'PRO')


class WorkStatus(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('ACTIVE', 'INACTIVE')


class WorkflowStatus(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('WIP', 'ACTIVE', 'ARCHIVED')


class YearOrderBy(sgqlc.types.Enum):
    __schema__ = shield
    __choices__ = ('year',)



########################################################################
# Input Objects
########################################################################
class AddIdentityProvidersToGroupInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'identity_provider_group_id', 'identity_provider_ids')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    identity_provider_group_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='identityProviderGroupId')
    identity_provider_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='identityProviderIds')


class AnimationInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('asset_url', 'name', 'static_image_url', 'text', 'tracking_pixel_url')
    asset_url = sgqlc.types.Field(String, graphql_name='assetUrl')
    name = sgqlc.types.Field(String, graphql_name='name')
    static_image_url = sgqlc.types.Field(String, graphql_name='staticImageUrl')
    text = sgqlc.types.Field(String, graphql_name='text')
    tracking_pixel_url = sgqlc.types.Field(String, graphql_name='trackingPixelUrl')


class ClearIdentityProviderGroupInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'identity_provider_group_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    identity_provider_group_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='identityProviderGroupId')


class CombineDataInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('bench_result', 'bench_result_video_ids', 'broad_jump_result', 'broad_jump_result_video_ids', 'combine_number', 'forty_yard_dash_result', 'forty_yard_dash_result_is_official', 'forty_yard_dash_result_video_ids', 'sixty_yard_shuttle_result', 'sixty_yard_shuttle_result_video_ids', 'three_cone_drill_result', 'three_cone_drill_result_video_ids', 'twenty_yard_shuttle_result', 'twenty_yard_shuttle_result_video_ids', 'vertical_jump_result', 'vertical_jump_result_video_ids')
    bench_result = sgqlc.types.Field(String, graphql_name='benchResult')
    bench_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='benchResultVideoIds')
    broad_jump_result = sgqlc.types.Field(String, graphql_name='broadJumpResult')
    broad_jump_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='broadJumpResultVideoIds')
    combine_number = sgqlc.types.Field(Int, graphql_name='combineNumber')
    forty_yard_dash_result = sgqlc.types.Field(String, graphql_name='fortyYardDashResult')
    forty_yard_dash_result_is_official = sgqlc.types.Field(Boolean, graphql_name='fortyYardDashResultIsOfficial')
    forty_yard_dash_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fortyYardDashResultVideoIds')
    sixty_yard_shuttle_result = sgqlc.types.Field(String, graphql_name='sixtyYardShuttleResult')
    sixty_yard_shuttle_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='sixtyYardShuttleResultVideoIds')
    three_cone_drill_result = sgqlc.types.Field(String, graphql_name='threeConeDrillResult')
    three_cone_drill_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='threeConeDrillResultVideoIds')
    twenty_yard_shuttle_result = sgqlc.types.Field(String, graphql_name='twentyYardShuttleResult')
    twenty_yard_shuttle_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='twentyYardShuttleResultVideoIds')
    vertical_jump_result = sgqlc.types.Field(String, graphql_name='verticalJumpResult')
    vertical_jump_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='verticalJumpResultVideoIds')


class CommonIdInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class CreateArticle(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'author_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_list_ids', 'description', 'element_ids', 'entitlement', 'event_ids', 'event_occurred_date', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'markdown_body', 'mobile_headline', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'series_ids', 'short_headline', 'show_ids', 'slug', 'tags', 'title', 'web_url', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    author_id = sgqlc.types.Field(String, graphql_name='authorId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    description = sgqlc.types.Field(String, graphql_name='description')
    element_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='elementIds')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    markdown_body = sgqlc.types.Field(String, graphql_name='markdownBody')
    mobile_headline = sgqlc.types.Field(String, graphql_name='mobileHeadline')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    series_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='seriesIds')
    short_headline = sgqlc.types.Field(String, graphql_name='shortHeadline')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    web_url = sgqlc.types.Field(String, graphql_name='webUrl')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateArticleInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('article', 'client_mutation_id')
    article = sgqlc.types.Field(sgqlc.types.non_null(CreateArticle), graphql_name='article')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateAudio(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'audio_asset_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_list_ids', 'description', 'entitlement', 'event_ids', 'event_occurred_date', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'series_ids', 'show_ids', 'slug', 'tags', 'title', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    audio_asset_id = sgqlc.types.Field(String, graphql_name='audioAssetId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    series_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='seriesIds')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateAudioAsset(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('attribution', 'available_to_properties_ids', 'encoding_date', 'entitlement', 'external_id', 'id', 'music', 'playback_url', 'playback_url2', 'property_id', 'runtime_secs', 'url')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    encoding_date = sgqlc.types.Field(DateTime, graphql_name='encodingDate')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    music = sgqlc.types.Field(sgqlc.types.list_of('MusicInput'), graphql_name='music')
    playback_url = sgqlc.types.Field(String, graphql_name='playbackUrl')
    playback_url2 = sgqlc.types.Field(String, graphql_name='playbackUrl2')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    runtime_secs = sgqlc.types.Field(Int, graphql_name='runtimeSecs')
    url = sgqlc.types.Field(String, graphql_name='url')


class CreateAudioAssetInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('audio_asset', 'client_mutation_id')
    audio_asset = sgqlc.types.Field(sgqlc.types.non_null(CreateAudioAsset), graphql_name='audioAsset')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateAudioInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('audio', 'client_mutation_id')
    audio = sgqlc.types.Field(CreateAudio, graphql_name='audio')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateAuthorPerson(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('bio', 'birth_date', 'birth_day', 'birth_month', 'birth_year', 'byline', 'college_name', 'death_day', 'death_month', 'death_year', 'deceased', 'display_name', 'first_name', 'headshot_image_id', 'high_school', 'hire_day', 'hire_month', 'hire_year', 'hometown', 'id', 'last_name', 'middle_name', 'nick_name', 'property_id', 'slug', 'socials', 'status', 'suffix', 'summary', 'work_status')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    byline = sgqlc.types.Field(String, graphql_name='byline')
    college_name = sgqlc.types.Field(String, graphql_name='collegeName')
    death_day = sgqlc.types.Field(Int, graphql_name='deathDay')
    death_month = sgqlc.types.Field(Int, graphql_name='deathMonth')
    death_year = sgqlc.types.Field(Int, graphql_name='deathYear')
    deceased = sgqlc.types.Field(Boolean, graphql_name='deceased')
    display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayName')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('SocialInput'), graphql_name='socials')
    status = sgqlc.types.Field(String, graphql_name='status')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CreateAuthorPersonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('author', 'client_mutation_id')
    author = sgqlc.types.Field(sgqlc.types.non_null(CreateAuthorPerson), graphql_name='author')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateBlackList(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('country_code', 'description', 'dma_code', 'identity_provider_id', 'network_name')
    country_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='countryCode')
    description = sgqlc.types.Field(String, graphql_name='description')
    dma_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dmaCode')
    identity_provider_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='identityProviderId')
    network_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='networkName')


class CreateBlackListInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('black_list', 'client_mutation_id')
    black_list = sgqlc.types.Field(sgqlc.types.non_null(CreateBlackList), graphql_name='blackList')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateCheerleader(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('cheerleader_person_id', 'id', 'season_id', 'season_value', 'team_id', 'tenure', 'title', 'title_description')
    cheerleader_person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cheerleaderPersonId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    season_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')


class CreateCheerleaderInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('cheerleader', 'client_mutation_id')
    cheerleader = sgqlc.types.Field(sgqlc.types.non_null(CreateCheerleader), graphql_name='cheerleader')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateCheerleaderPerson(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('bio', 'birth_date', 'birth_day', 'birth_month', 'birth_year', 'college_name', 'death_day', 'death_month', 'death_year', 'deceased', 'display_name', 'eye_color', 'first_name', 'hair_color', 'headshot_image_id', 'high_school', 'hire_day', 'hire_month', 'hire_year', 'hometown', 'id', 'large_image_id', 'last_name', 'link_page', 'middle_name', 'nfl_experience', 'nick_name', 'occupation', 'property_id', 'slug', 'socials', 'status', 'suffix', 'summary', 'tenure', 'work_status')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    college_name = sgqlc.types.Field(String, graphql_name='collegeName')
    death_day = sgqlc.types.Field(Int, graphql_name='deathDay')
    death_month = sgqlc.types.Field(Int, graphql_name='deathMonth')
    death_year = sgqlc.types.Field(Int, graphql_name='deathYear')
    deceased = sgqlc.types.Field(Boolean, graphql_name='deceased')
    display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayName')
    eye_color = sgqlc.types.Field(String, graphql_name='eyeColor')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    hair_color = sgqlc.types.Field(String, graphql_name='hairColor')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    large_image_id = sgqlc.types.Field(String, graphql_name='largeImageId')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    occupation = sgqlc.types.Field(String, graphql_name='occupation')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('SocialInput'), graphql_name='socials')
    status = sgqlc.types.Field(String, graphql_name='status')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    tenure = sgqlc.types.Field(String, graphql_name='tenure')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CreateCheerleaderPersonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('cheerleader_person', 'client_mutation_id')
    cheerleader_person = sgqlc.types.Field(sgqlc.types.non_null(CreateCheerleaderPerson), graphql_name='cheerleaderPerson')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class CreateClubInjuryReport(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('display_name', 'headshot_image_url', 'injuries', 'injury_status', 'player_id', 'position', 'practice_statuses', 'practices', 'team_id', 'week_id')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    headshot_image_url = sgqlc.types.Field(String, graphql_name='headshotImageUrl')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='injuries')
    injury_status = sgqlc.types.Field(InjuryStatus, graphql_name='injuryStatus')
    player_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='playerId')
    position = sgqlc.types.Field(String, graphql_name='position')
    practice_statuses = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practiceStatuses')
    practices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practices')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')
    week_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='weekId')


class CreateClubInjuryReportInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'club_injury_report')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    club_injury_report = sgqlc.types.Field(sgqlc.types.non_null(CreateClubInjuryReport), graphql_name='clubInjuryReport')


class CreateClubTransaction(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('available_to_properties_ids', 'franchise_id', 'id', 'last_publish_date', 'original_publish_date', 'publish_state', 'repository', 'transaction_day', 'transaction_detail', 'transaction_month', 'transaction_year', 'workflow_status')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    franchise_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='franchiseId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    transaction_day = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='transactionDay')
    transaction_detail = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='transactionDetail')
    transaction_month = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='transactionMonth')
    transaction_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='transactionYear')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateClubTransactionInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'club_transaction')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    club_transaction = sgqlc.types.Field(sgqlc.types.non_null(CreateClubTransaction), graphql_name='clubTransaction')


class CreateCoach(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('coach_person_id', 'id', 'season_id', 'season_value', 'team_id', 'tenure', 'title', 'title_description', 'unit')
    coach_person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='coachPersonId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    season_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')
    unit = sgqlc.types.Field(Platoon, graphql_name='unit')


class CreateCoachInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'coach')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    coach = sgqlc.types.Field(sgqlc.types.non_null(CreateCoach), graphql_name='coach')


class CreateCoachPerson(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('bio', 'birth_date', 'birth_day', 'birth_month', 'birth_year', 'coach_type', 'college_name', 'death_day', 'death_month', 'death_year', 'deceased', 'display_name', 'first_name', 'headshot_image_id', 'high_school', 'hire_day', 'hire_month', 'hire_year', 'hometown', 'id', 'last_name', 'link_page', 'middle_name', 'nfl_experience', 'nick_name', 'property_id', 'slug', 'socials', 'status', 'suffix', 'summary', 'work_status')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    coach_type = sgqlc.types.Field(CoachType, graphql_name='coachType')
    college_name = sgqlc.types.Field(String, graphql_name='collegeName')
    death_day = sgqlc.types.Field(Int, graphql_name='deathDay')
    death_month = sgqlc.types.Field(Int, graphql_name='deathMonth')
    death_year = sgqlc.types.Field(Int, graphql_name='deathYear')
    deceased = sgqlc.types.Field(Boolean, graphql_name='deceased')
    display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayName')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('SocialInput'), graphql_name='socials')
    status = sgqlc.types.Field(String, graphql_name='status')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CreateCoachPersonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'coach_person')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    coach_person = sgqlc.types.Field(sgqlc.types.non_null(CreateCoachPerson), graphql_name='coachPerson')


class CreateContent(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('content_type', 'id', 'summary', 'tags', 'title', 'url')
    content_type = sgqlc.types.Field(sgqlc.types.non_null(ContentType), graphql_name='contentType')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    tags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class CreateContentInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'content', 'property_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    content = sgqlc.types.Field(sgqlc.types.non_null(CreateContent), graphql_name='content')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class CreateContentList(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'author_ids', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_hints', 'content_ids', 'content_ids_to_add', 'content_ids_to_remove', 'content_list_ids', 'content_query', 'curation', 'description', 'entitlement', 'event_ids', 'external_id', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'materialization_hint', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'series_ids', 'show_ids', 'slug', 'tags', 'title', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    author_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='authorIds')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_hints = sgqlc.types.Field(sgqlc.types.list_of(ContentHint), graphql_name='contentHints')
    content_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentIds')
    content_ids_to_add = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentIdsToAdd')
    content_ids_to_remove = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentIdsToRemove')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    content_query = sgqlc.types.Field(String, graphql_name='contentQuery')
    curation = sgqlc.types.Field(Curation, graphql_name='curation')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    materialization_hint = sgqlc.types.Field(MaterializationHint, graphql_name='materializationHint')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    series_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='seriesIds')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateContentListInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'content_list')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    content_list = sgqlc.types.Field(sgqlc.types.non_null(CreateContentList), graphql_name='contentList')


class CreateCurrentClubDepthChart(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('depth_num', 'depth_num_label', 'display_name', 'first_name', 'last_name', 'person_id', 'platoon', 'platoon_label', 'position', 'position_label', 'property_id')
    depth_num = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='depthNum')
    depth_num_label = sgqlc.types.Field(String, graphql_name='depthNumLabel')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    person_id = sgqlc.types.Field(String, graphql_name='personId')
    platoon = sgqlc.types.Field(sgqlc.types.non_null(Platoon), graphql_name='platoon')
    platoon_label = sgqlc.types.Field(String, graphql_name='platoonLabel')
    position = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='position')
    position_label = sgqlc.types.Field(String, graphql_name='positionLabel')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class CreateCurrentClubDepthChartInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'current_club_depth_chart')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    current_club_depth_chart = sgqlc.types.Field(sgqlc.types.non_null(CreateCurrentClubDepthChart), graphql_name='currentClubDepthChart')


class CreateCurrentClubRoster(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('birth_day', 'birth_month', 'birth_year', 'college', 'display_name', 'first_name', 'headshot_image_url', 'height', 'jersey_number', 'last_name', 'nfl_experience', 'person_id', 'position', 'property_id', 'status', 'weight')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    college = sgqlc.types.Field(String, graphql_name='college')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    headshot_image_url = sgqlc.types.Field(String, graphql_name='headshotImageUrl')
    height = sgqlc.types.Field(String, graphql_name='height')
    jersey_number = sgqlc.types.Field(Int, graphql_name='jerseyNumber')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='personId')
    position = sgqlc.types.Field(String, graphql_name='position')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    status = sgqlc.types.Field(String, graphql_name='status')
    weight = sgqlc.types.Field(Int, graphql_name='weight')


class CreateCurrentClubRosterInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'current_club_roster')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    current_club_roster = sgqlc.types.Field(sgqlc.types.non_null(CreateCurrentClubRoster), graphql_name='currentClubRoster')


class CreateCurrentContextual(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('context', 'type', 'value')
    context = sgqlc.types.Field(CurrentContext, graphql_name='context')
    type = sgqlc.types.Field(CurrentType, graphql_name='type')
    value = sgqlc.types.Field(String, graphql_name='value')


class CreateCurrentContextualInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'current_contextual')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    current_contextual = sgqlc.types.Field(sgqlc.types.non_null(CreateCurrentContextual), graphql_name='currentContextual')


class CreateDepthChartPositionOrder(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('position_order', 'property_id')
    position_order = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='positionOrder')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class CreateDepthChartPositionOrderInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'depth_chart_position_order')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    depth_chart_position_order = sgqlc.types.Field(sgqlc.types.non_null(CreateDepthChartPositionOrder), graphql_name='depthChartPositionOrder')


class CreateDraft(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('complete', 'current_pick', 'current_round', 'draft_state', 'id', 'name', 'team_on_the_clock_id', 'venue_id', 'year')
    complete = sgqlc.types.Field(Boolean, graphql_name='complete')
    current_pick = sgqlc.types.Field(Int, graphql_name='currentPick')
    current_round = sgqlc.types.Field(Int, graphql_name='currentRound')
    draft_state = sgqlc.types.Field(DraftState, graphql_name='draftState')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    team_on_the_clock_id = sgqlc.types.Field(String, graphql_name='teamOnTheClockId')
    venue_id = sgqlc.types.Field(String, graphql_name='venueId')
    year = sgqlc.types.Field(Int, graphql_name='year')


class CreateDraftInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'draft')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    draft = sgqlc.types.Field(sgqlc.types.non_null(CreateDraft), graphql_name='draft')


class CreateDraftPick(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analysis', 'draft_number_overall', 'draft_player_position', 'draft_position', 'draft_round', 'draft_team_id', 'draft_type', 'draft_year', 'pick_is_in', 'player_id', 'prospect_id', 'trade_note')
    analysis = sgqlc.types.Field(String, graphql_name='analysis')
    draft_number_overall = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftNumberOverall')
    draft_player_position = sgqlc.types.Field(String, graphql_name='draftPlayerPosition')
    draft_position = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftPosition')
    draft_round = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftRound')
    draft_team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='draftTeamId')
    draft_type = sgqlc.types.Field(String, graphql_name='draftType')
    draft_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftYear')
    pick_is_in = sgqlc.types.Field(Boolean, graphql_name='pickIsIn')
    player_id = sgqlc.types.Field(String, graphql_name='playerId')
    prospect_id = sgqlc.types.Field(String, graphql_name='prospectId')
    trade_note = sgqlc.types.Field(String, graphql_name='tradeNote')


class CreateDraftPickInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'draft_pick', 'insert_additional_draft_pick')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    draft_pick = sgqlc.types.Field(CreateDraftPick, graphql_name='draftPick')
    insert_additional_draft_pick = sgqlc.types.Field(CreateDraftPick, graphql_name='insertAdditionalDraftPick')


class CreateDraftTeam(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('franchise_id', 'grade', 'id', 'needs', 'needs_by_position_cb', 'needs_by_position_dl', 'needs_by_position_lb', 'needs_by_position_ol', 'needs_by_position_qb', 'needs_by_position_rb', 'needs_by_position_spec', 'needs_by_position_te', 'needs_by_position_wr', 'notes', 'position_needs', 'post_draft_assessment', 'ticket_url', 'year')
    franchise_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='franchiseId')
    grade = sgqlc.types.Field(String, graphql_name='grade')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    needs = sgqlc.types.Field(Int, graphql_name='needs')
    needs_by_position_cb = sgqlc.types.Field(Int, graphql_name='needsByPositionCB')
    needs_by_position_dl = sgqlc.types.Field(Int, graphql_name='needsByPositionDL')
    needs_by_position_lb = sgqlc.types.Field(Int, graphql_name='needsByPositionLB')
    needs_by_position_ol = sgqlc.types.Field(Int, graphql_name='needsByPositionOL')
    needs_by_position_qb = sgqlc.types.Field(Int, graphql_name='needsByPositionQB')
    needs_by_position_rb = sgqlc.types.Field(Int, graphql_name='needsByPositionRB')
    needs_by_position_spec = sgqlc.types.Field(Int, graphql_name='needsByPositionSpec')
    needs_by_position_te = sgqlc.types.Field(Int, graphql_name='needsByPositionTE')
    needs_by_position_wr = sgqlc.types.Field(Int, graphql_name='needsByPositionWR')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    position_needs = sgqlc.types.Field(String, graphql_name='positionNeeds')
    post_draft_assessment = sgqlc.types.Field(String, graphql_name='postDraftAssessment')
    ticket_url = sgqlc.types.Field(String, graphql_name='ticketUrl')
    year = sgqlc.types.Field(Int, graphql_name='year')


class CreateDraftTeamInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'draft_team')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    draft_team = sgqlc.types.Field(sgqlc.types.non_null(CreateDraftTeam), graphql_name='draftTeam')


class CreateEliasProspect(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('arm_length', 'background_image_id', 'birth_city', 'birth_date', 'birth_state', 'bottom_line', 'college_class', 'college_conference', 'college_experience', 'college_jersey_number', 'colleges', 'combine_data', 'current_college', 'display_hint', 'draft_id', 'draft_position', 'draft_projection', 'draft_round', 'draft_year', 'elias_college_id', 'elias_home_country', 'elias_position', 'elias_position_id', 'elias_team_id', 'first_name', 'full_first_name', 'grade', 'grade_rubric', 'hand_size', 'headshot_image_id', 'height', 'high_school', 'home_state', 'hometown', 'last_name', 'middle_name', 'nfl_comparison', 'overview', 'position', 'position_depth', 'profile_author', 'sources_tell_us', 'strengths', 'suffix', 'video_id', 'weaknesses', 'weight', 'year', 'years_of_eligibility_left')
    arm_length = sgqlc.types.Field(String, graphql_name='armLength')
    background_image_id = sgqlc.types.Field(String, graphql_name='backgroundImageId')
    birth_city = sgqlc.types.Field(String, graphql_name='birthCity')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_state = sgqlc.types.Field(String, graphql_name='birthState')
    bottom_line = sgqlc.types.Field(String, graphql_name='bottomLine')
    college_class = sgqlc.types.Field(String, graphql_name='collegeClass')
    college_conference = sgqlc.types.Field(String, graphql_name='collegeConference')
    college_experience = sgqlc.types.Field(Int, graphql_name='collegeExperience')
    college_jersey_number = sgqlc.types.Field(String, graphql_name='collegeJerseyNumber')
    colleges = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='colleges')
    combine_data = sgqlc.types.Field(CombineDataInput, graphql_name='combineData')
    current_college = sgqlc.types.Field(String, graphql_name='currentCollege')
    display_hint = sgqlc.types.Field(DisplayHint, graphql_name='displayHint')
    draft_id = sgqlc.types.Field(String, graphql_name='draftId')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_projection = sgqlc.types.Field(String, graphql_name='draftProjection')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    elias_college_id = sgqlc.types.Field(Int, graphql_name='eliasCollegeId')
    elias_home_country = sgqlc.types.Field(String, graphql_name='eliasHomeCountry')
    elias_position = sgqlc.types.Field(String, graphql_name='eliasPosition')
    elias_position_id = sgqlc.types.Field(Int, graphql_name='eliasPositionId')
    elias_team_id = sgqlc.types.Field(Int, graphql_name='eliasTeamId')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    full_first_name = sgqlc.types.Field(String, graphql_name='fullFirstName')
    grade = sgqlc.types.Field(Float, graphql_name='grade')
    grade_rubric = sgqlc.types.Field(String, graphql_name='gradeRubric')
    hand_size = sgqlc.types.Field(String, graphql_name='handSize')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    height = sgqlc.types.Field(String, graphql_name='height')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    home_state = sgqlc.types.Field(String, graphql_name='homeState')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    last_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='lastName')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nfl_comparison = sgqlc.types.Field(String, graphql_name='nflComparison')
    overview = sgqlc.types.Field(String, graphql_name='overview')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_depth = sgqlc.types.Field(Int, graphql_name='positionDepth')
    profile_author = sgqlc.types.Field(String, graphql_name='profileAuthor')
    sources_tell_us = sgqlc.types.Field(String, graphql_name='sourcesTellUs')
    strengths = sgqlc.types.Field(String, graphql_name='strengths')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    video_id = sgqlc.types.Field(String, graphql_name='videoId')
    weaknesses = sgqlc.types.Field(String, graphql_name='weaknesses')
    weight = sgqlc.types.Field(String, graphql_name='weight')
    year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='year')
    years_of_eligibility_left = sgqlc.types.Field(Int, graphql_name='yearsOfEligibilityLeft')


class CreateEliasProspectInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'elias_prospect')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    elias_prospect = sgqlc.types.Field(sgqlc.types.non_null(CreateEliasProspect), graphql_name='eliasProspect')


class CreateEvent(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('active', 'analytics_id', 'audio_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_list_ids', 'cta_button_text', 'cta_link', 'cta_second_button_text', 'cta_second_link', 'days_of_week', 'description', 'end_date', 'end_time', 'entitlement', 'event_ids', 'event_type', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'location', 'location_url', 'name', 'online', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'property_id', 'publish_state', 'recurrence', 'repository', 'season_id', 'season_value', 'show_ids', 'slug', 'start_date', 'start_time', 'tags', 'title', 'video_id', 'workflow_status')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    audio_id = sgqlc.types.Field(String, graphql_name='audioId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    cta_button_text = sgqlc.types.Field(String, graphql_name='ctaButtonText')
    cta_link = sgqlc.types.Field(String, graphql_name='ctaLink')
    cta_second_button_text = sgqlc.types.Field(String, graphql_name='ctaSecondButtonText')
    cta_second_link = sgqlc.types.Field(String, graphql_name='ctaSecondLink')
    days_of_week = sgqlc.types.Field(sgqlc.types.list_of(DayOfWeek), graphql_name='daysOfWeek')
    description = sgqlc.types.Field(String, graphql_name='description')
    end_date = sgqlc.types.Field(DateTime, graphql_name='endDate')
    end_time = sgqlc.types.Field(DateTime, graphql_name='endTime')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    event_type = sgqlc.types.Field(EventType, graphql_name='eventType')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    location = sgqlc.types.Field(String, graphql_name='location')
    location_url = sgqlc.types.Field(String, graphql_name='locationUrl')
    name = sgqlc.types.Field(String, graphql_name='name')
    online = sgqlc.types.Field(Boolean, graphql_name='online')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    recurrence = sgqlc.types.Field(Recurrence, graphql_name='recurrence')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    start_date = sgqlc.types.Field(DateTime, graphql_name='startDate')
    start_time = sgqlc.types.Field(DateTime, graphql_name='startTime')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    video_id = sgqlc.types.Field(String, graphql_name='videoId')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateEventInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'event')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    event = sgqlc.types.Field(sgqlc.types.non_null(CreateEvent), graphql_name='event')


class CreateExecutive(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('department', 'executive_person_id', 'id', 'season_id', 'season_value', 'team_id', 'tenure', 'title', 'title_description')
    department = sgqlc.types.Field(String, graphql_name='department')
    executive_person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='executivePersonId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    season_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')


class CreateExecutiveInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'executive')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    executive = sgqlc.types.Field(sgqlc.types.non_null(CreateExecutive), graphql_name='executive')


class CreateExecutivePerson(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('bio', 'birth_date', 'birth_day', 'birth_month', 'birth_year', 'college_name', 'death_day', 'death_month', 'death_year', 'deceased', 'display_name', 'first_name', 'headshot_image_id', 'high_school', 'hire_day', 'hire_month', 'hire_year', 'hometown', 'id', 'last_name', 'link_page', 'middle_name', 'nfl_experience', 'nick_name', 'property_id', 'slug', 'socials', 'status', 'suffix', 'summary', 'work_status')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    college_name = sgqlc.types.Field(String, graphql_name='collegeName')
    death_day = sgqlc.types.Field(Int, graphql_name='deathDay')
    death_month = sgqlc.types.Field(Int, graphql_name='deathMonth')
    death_year = sgqlc.types.Field(Int, graphql_name='deathYear')
    deceased = sgqlc.types.Field(Boolean, graphql_name='deceased')
    display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayName')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('SocialInput'), graphql_name='socials')
    status = sgqlc.types.Field(String, graphql_name='status')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CreateExecutivePersonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'executive_person')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    executive_person = sgqlc.types.Field(sgqlc.types.non_null(CreateExecutivePerson), graphql_name='executivePerson')


class CreateGame(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('away_team_id', 'category', 'esb_id', 'game_time', 'gsis_id', 'home_team_id', 'id', 'network_channels', 'radio_links', 'territory', 'ticket_url', 'venue_id', 'week_id')
    away_team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='awayTeamId')
    category = sgqlc.types.Field(String, graphql_name='category')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    game_time = sgqlc.types.Field(DateTime, graphql_name='gameTime')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    home_team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='homeTeamId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    network_channels = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='networkChannels')
    radio_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='radioLinks')
    territory = sgqlc.types.Field(String, graphql_name='territory')
    ticket_url = sgqlc.types.Field(String, graphql_name='ticketUrl')
    venue_id = sgqlc.types.Field(String, graphql_name='venueId')
    week_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='weekId')


class CreateGameInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'game')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    game = sgqlc.types.Field(sgqlc.types.non_null(CreateGame), graphql_name='game')


class CreateIdentityProvider(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('adobe_mso_id', 'app_url_android', 'app_url_ios', 'auth_provider_id', 'display_name', 'display_order', 'enabled', 'id', 'identity_provider_group_ids', 'logo_url', 'max_streams', 'name', 'tms_mso_id', 'type', 'website')
    adobe_mso_id = sgqlc.types.Field(String, graphql_name='adobeMsoId')
    app_url_android = sgqlc.types.Field(String, graphql_name='appUrlAndroid')
    app_url_ios = sgqlc.types.Field(String, graphql_name='appUrlIos')
    auth_provider_id = sgqlc.types.Field(String, graphql_name='authProviderId')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    display_order = sgqlc.types.Field(Int, graphql_name='displayOrder')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    identity_provider_group_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='identityProviderGroupIds')
    logo_url = sgqlc.types.Field(String, graphql_name='logoUrl')
    max_streams = sgqlc.types.Field(Int, graphql_name='maxStreams')
    name = sgqlc.types.Field(String, graphql_name='name')
    tms_mso_id = sgqlc.types.Field(String, graphql_name='tmsMsoId')
    type = sgqlc.types.Field(String, graphql_name='type')
    website = sgqlc.types.Field(String, graphql_name='website')


class CreateIdentityProviderGroup(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('auth_provider_id', 'identity_provider_ids', 'logo_url', 'name', 'priority')
    auth_provider_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='authProviderId')
    identity_provider_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='identityProviderIds')
    logo_url = sgqlc.types.Field(String, graphql_name='logoUrl')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    priority = sgqlc.types.Field(Int, graphql_name='priority')


class CreateIdentityProviderGroupInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'identity_provider_group')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    identity_provider_group = sgqlc.types.Field(sgqlc.types.non_null(CreateIdentityProviderGroup), graphql_name='identityProviderGroup')


class CreateIdentityProviderInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'identity_provider')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    identity_provider = sgqlc.types.Field(sgqlc.types.non_null(CreateIdentityProvider), graphql_name='identityProvider')


class CreateImage(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'attribution', 'author_byline', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_list_ids', 'copyright', 'description', 'entitlement', 'event_ids', 'external_id', 'file_name', 'for_purchase', 'franchise_ids', 'game_ids', 'id', 'image_asset_id', 'image_type', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'photographer_name', 'play_id', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'show_ids', 'slug', 'tags', 'title', 'url', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    author_byline = sgqlc.types.Field(String, graphql_name='authorByline')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    copyright = sgqlc.types.Field(String, graphql_name='copyright')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    file_name = sgqlc.types.Field(String, graphql_name='fileName')
    for_purchase = sgqlc.types.Field(ForPurchase, graphql_name='forPurchase')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_asset_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='imageAssetId')
    image_type = sgqlc.types.Field(ImageType, graphql_name='imageType')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    photographer_name = sgqlc.types.Field(String, graphql_name='photographerName')
    play_id = sgqlc.types.Field('PlayId', graphql_name='playId')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateImageAsset(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('attribution', 'author_byline', 'available_to_properties_ids', 'caption', 'entitlement', 'external_id', 'id', 'photographer_name', 'property_id', 'title', 'url')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    author_byline = sgqlc.types.Field(String, graphql_name='authorByline')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    photographer_name = sgqlc.types.Field(String, graphql_name='photographerName')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    title = sgqlc.types.Field(String, graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')


class CreateImageAssetInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'image_asset')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    image_asset = sgqlc.types.Field(sgqlc.types.non_null(CreateImageAsset), graphql_name='imageAsset')


class CreateImageInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'image')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    image = sgqlc.types.Field(sgqlc.types.non_null(CreateImage), graphql_name='image')


class CreateInjuryReport(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('club_reported_injuries', 'id', 'team_id', 'week_id')
    club_reported_injuries = sgqlc.types.Field(sgqlc.types.list_of('InjuredPlayerInput'), graphql_name='clubReportedInjuries')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')
    week_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='weekId')


class CreateInjuryReportInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'injury_report')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    injury_report = sgqlc.types.Field(sgqlc.types.non_null(CreateInjuryReport), graphql_name='injuryReport')


class CreateKeyword(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('keyword', 'metadata', 'url')
    keyword = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='keyword')
    metadata = sgqlc.types.Field(Map, graphql_name='metadata')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class CreateKeywordInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'keyword', 'property_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    keyword = sgqlc.types.Field(sgqlc.types.non_null(CreateKeyword), graphql_name='keyword')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class CreateMeta(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('entity_id', 'entity_type', 'entries')
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='entityId')
    entity_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='entityType')
    entries = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('StringMapInput')), graphql_name='entries')


class CreateMetaInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'meta')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    meta = sgqlc.types.Field(sgqlc.types.non_null(CreateMeta), graphql_name='meta')


class CreateMilestonePlayer(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'game_detail_id', 'gsis_player_id', 'milestone_type', 'milestone_value', 'person_id')
    current_team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='currentTeamId')
    game_detail_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='gameDetailId')
    gsis_player_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='gsisPlayerId')
    milestone_type = sgqlc.types.Field(sgqlc.types.non_null(MilestoneType), graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='milestoneValue')
    person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='personId')


class CreateMilestonePlayerInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'milestone_player')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    milestone_player = sgqlc.types.Field(sgqlc.types.non_null(CreateMilestonePlayer), graphql_name='milestonePlayer')


class CreateMilestoneTeam(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'milestone_type', 'milestone_value', 'team_id')
    game_detail_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='gameDetailId')
    milestone_type = sgqlc.types.Field(sgqlc.types.non_null(MilestoneType), graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='milestoneValue')
    team_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamId')


class CreateMilestoneTeamInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'milestone_team')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    milestone_team = sgqlc.types.Field(sgqlc.types.non_null(CreateMilestoneTeam), graphql_name='milestoneTeam')


class CreateMockDraft(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('author_id', 'caption', 'draft_pick_ids', 'id', 'title', 'version', 'video_id', 'year')
    author_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='authorId')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    draft_pick_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='draftPickIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    version = sgqlc.types.Field(String, graphql_name='version')
    video_id = sgqlc.types.Field(String, graphql_name='videoId')
    year = sgqlc.types.Field(Int, graphql_name='year')


class CreateMockDraftInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'mock_draft')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    mock_draft = sgqlc.types.Field(sgqlc.types.non_null(CreateMockDraft), graphql_name='mockDraft')


class CreateMockDraftPick(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analysis', 'franchise_id', 'id', 'pick_number', 'prospect_id')
    analysis = sgqlc.types.Field(String, graphql_name='analysis')
    franchise_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='franchiseId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    pick_number = sgqlc.types.Field(Int, graphql_name='pickNumber')
    prospect_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='prospectId')


class CreateMockDraftPickInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'mock_draft_pick')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    mock_draft_pick = sgqlc.types.Field(sgqlc.types.non_null(CreateMockDraftPick), graphql_name='mockDraftPick')


class CreatePersonList(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'content_list_ids', 'description', 'entitlement', 'event_ids', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'materialization_hint', 'original_publish_date', 'origination', 'permalink', 'person_id_list', 'person_ids', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'show_ids', 'slug', 'tags', 'title', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    materialization_hint = sgqlc.types.Field(MaterializationHint, graphql_name='materializationHint')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_id_list = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIdList')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreatePersonListInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'person_list')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    person_list = sgqlc.types.Field(sgqlc.types.non_null(CreatePersonList), graphql_name='personList')


class CreatePromo(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'available_to_properties_ids', 'available_to_property_ids', 'background_image_id', 'caption', 'content_category', 'content_list_ids', 'cta_button_text', 'cta_link', 'cta_second_button_text', 'cta_second_link', 'description', 'entitlement', 'event_ids', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'property_id', 'publish_state', 'repository', 'season_id', 'season_value', 'show_ids', 'slug', 'tags', 'title', 'url', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    background_image_id = sgqlc.types.Field(String, graphql_name='backgroundImageId')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    content_category = sgqlc.types.Field(String, graphql_name='contentCategory')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    cta_button_text = sgqlc.types.Field(String, graphql_name='ctaButtonText')
    cta_link = sgqlc.types.Field(String, graphql_name='ctaLink')
    cta_second_button_text = sgqlc.types.Field(String, graphql_name='ctaSecondButtonText')
    cta_second_link = sgqlc.types.Field(String, graphql_name='ctaSecondLink')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreatePromoInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'promo')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    promo = sgqlc.types.Field(sgqlc.types.non_null(CreatePromo), graphql_name='promo')


class CreateProspect(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('arm_length', 'background_image_id', 'bottom_line', 'college_class', 'college_conference', 'college_experience', 'college_jersey_number', 'colleges', 'combine_data', 'current_college', 'display_hint', 'draft_id', 'draft_position', 'draft_projection', 'draft_round', 'draft_year', 'grade', 'grade_rubric', 'hand_size', 'headshot_image_id', 'height', 'home_state', 'id', 'nfl_comparison', 'overview', 'person_id', 'position', 'position_depth', 'profile_author', 'sources_tell_us', 'strengths', 'video_id', 'weaknesses', 'weight', 'year', 'years_of_eligibility_left')
    arm_length = sgqlc.types.Field(String, graphql_name='armLength')
    background_image_id = sgqlc.types.Field(String, graphql_name='backgroundImageId')
    bottom_line = sgqlc.types.Field(String, graphql_name='bottomLine')
    college_class = sgqlc.types.Field(String, graphql_name='collegeClass')
    college_conference = sgqlc.types.Field(String, graphql_name='collegeConference')
    college_experience = sgqlc.types.Field(Int, graphql_name='collegeExperience')
    college_jersey_number = sgqlc.types.Field(String, graphql_name='collegeJerseyNumber')
    colleges = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='colleges')
    combine_data = sgqlc.types.Field(CombineDataInput, graphql_name='combineData')
    current_college = sgqlc.types.Field(String, graphql_name='currentCollege')
    display_hint = sgqlc.types.Field(DisplayHint, graphql_name='displayHint')
    draft_id = sgqlc.types.Field(String, graphql_name='draftId')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_projection = sgqlc.types.Field(String, graphql_name='draftProjection')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    grade = sgqlc.types.Field(Float, graphql_name='grade')
    grade_rubric = sgqlc.types.Field(String, graphql_name='gradeRubric')
    hand_size = sgqlc.types.Field(String, graphql_name='handSize')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    height = sgqlc.types.Field(String, graphql_name='height')
    home_state = sgqlc.types.Field(String, graphql_name='homeState')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    nfl_comparison = sgqlc.types.Field(String, graphql_name='nflComparison')
    overview = sgqlc.types.Field(String, graphql_name='overview')
    person_id = sgqlc.types.Field(String, graphql_name='personId')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_depth = sgqlc.types.Field(Int, graphql_name='positionDepth')
    profile_author = sgqlc.types.Field(String, graphql_name='profileAuthor')
    sources_tell_us = sgqlc.types.Field(String, graphql_name='sourcesTellUs')
    strengths = sgqlc.types.Field(String, graphql_name='strengths')
    video_id = sgqlc.types.Field(String, graphql_name='videoId')
    weaknesses = sgqlc.types.Field(String, graphql_name='weaknesses')
    weight = sgqlc.types.Field(String, graphql_name='weight')
    year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='year')
    years_of_eligibility_left = sgqlc.types.Field(Int, graphql_name='yearsOfEligibilityLeft')


class CreateProspectInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'prospect')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    prospect = sgqlc.types.Field(sgqlc.types.non_null(CreateProspect), graphql_name='prospect')


class CreateSeason(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('id', 'season')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    season = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='season')


class CreateSeasonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'season')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    season = sgqlc.types.Field(sgqlc.types.non_null(CreateSeason), graphql_name='season')


class CreateSeries(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('advertiser_frequency', 'advertiser_id', 'advertiser_text', 'id', 'last_publish_date', 'original_publish_date', 'pinned_content_ids', 'property_id', 'publish_state', 'series_theme', 'thumbnail_image_id', 'title', 'type', 'workflow_status')
    advertiser_frequency = sgqlc.types.Field(Int, graphql_name='advertiserFrequency')
    advertiser_id = sgqlc.types.Field(String, graphql_name='advertiserId')
    advertiser_text = sgqlc.types.Field(String, graphql_name='advertiserText')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    pinned_content_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='pinnedContentIds')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    series_theme = sgqlc.types.Field(String, graphql_name='seriesTheme')
    thumbnail_image_id = sgqlc.types.Field(String, graphql_name='thumbnailImageId')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    type = sgqlc.types.Field(SeriesType, graphql_name='type')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateSeriesInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'series')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    series = sgqlc.types.Field(sgqlc.types.non_null(CreateSeries), graphql_name='series')


class CreateShow(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('id', 'name', 'property_id', 'workflow_status')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateShowInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'show')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    show = sgqlc.types.Field(sgqlc.types.non_null(CreateShow), graphql_name='show')


class CreateTag(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('advertiser_id', 'id', 'property_id', 'tag')
    advertiser_id = sgqlc.types.Field(String, graphql_name='advertiserId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    tag = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='tag')


class CreateTagInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'tag')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    tag = sgqlc.types.Field(sgqlc.types.non_null(CreateTag), graphql_name='tag')


class CreateTeam(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('abbreviation', 'city_state_region', 'coach_ids', 'conference', 'depth_chart_ids', 'division', 'franchise_id', 'full_name', 'id', 'logo_image_id', 'market_zip_code', 'nick_name', 'player_ids', 'season_id', 'season_value', 'team_type', 'venue_ids')
    abbreviation = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='abbreviation')
    city_state_region = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cityStateRegion')
    coach_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='coachIds')
    conference = sgqlc.types.Field(sgqlc.types.non_null(Conference), graphql_name='conference')
    depth_chart_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='depthChartIds')
    division = sgqlc.types.Field(sgqlc.types.non_null(Division), graphql_name='division')
    franchise_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='franchiseId')
    full_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fullName')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    logo_image_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='logoImageId')
    market_zip_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='marketZipCode')
    nick_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nickName')
    player_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='playerIds')
    season_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='seasonId')
    season_value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='seasonValue')
    team_type = sgqlc.types.Field(sgqlc.types.non_null(TeamType), graphql_name='teamType')
    venue_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='venueIds')


class CreateTeamInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'team')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    team = sgqlc.types.Field(sgqlc.types.non_null(CreateTeam), graphql_name='team')


class CreateVideo(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'clip_type', 'content_list_ids', 'description', 'entitlement', 'event_ids', 'event_occurred_date', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'pre_roll_enabled', 'primary_channel', 'property_id', 'publish_state', 'related_play_ids', 'repository', 'season_id', 'season_value', 'series_ids', 'show_ids', 'slug', 'tags', 'title', 'video_asset_id', 'week_id', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    clip_type = sgqlc.types.Field(ClipType, graphql_name='clipType')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    pre_roll_enabled = sgqlc.types.Field(Boolean, graphql_name='preRollEnabled')
    primary_channel = sgqlc.types.Field(String, graphql_name='primaryChannel')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    related_play_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayId'), graphql_name='relatedPlayIds')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    series_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='seriesIds')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    video_asset_id = sgqlc.types.Field(String, graphql_name='videoAssetId')
    week_id = sgqlc.types.Field(String, graphql_name='weekId')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class CreateVideoAsset(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('attribution', 'available_to_properties_ids', 'encoding_date', 'entitlement', 'external_id', 'id', 'music', 'playback_url', 'property_id', 'runtime_secs', 'url')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    encoding_date = sgqlc.types.Field(DateTime, graphql_name='encodingDate')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    music = sgqlc.types.Field(sgqlc.types.list_of('MusicInput'), graphql_name='music')
    playback_url = sgqlc.types.Field(String, graphql_name='playbackUrl')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    runtime_secs = sgqlc.types.Field(Int, graphql_name='runtimeSecs')
    url = sgqlc.types.Field(String, graphql_name='url')


class CreateVideoAssetInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'video_asset')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    video_asset = sgqlc.types.Field(sgqlc.types.non_null(CreateVideoAsset), graphql_name='videoAsset')


class CreateVideoInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'video')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    video = sgqlc.types.Field(sgqlc.types.non_null(CreateVideo), graphql_name='video')


class DeleteBlackList(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('country_code', 'dma_code', 'identity_provider_id', 'network')
    country_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='countryCode')
    dma_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dmaCode')
    identity_provider_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='identityProviderId')
    network = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='network')


class DeleteBlackListInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('black_list', 'client_mutation_id')
    black_list = sgqlc.types.Field(sgqlc.types.non_null(DeleteBlackList), graphql_name='blackList')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class DeleteCelebrationInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('celebration_id', 'client_mutation_id')
    celebration_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='celebrationId')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class DeleteCurrentClubDepthChart(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('depth_num', 'platoon', 'position', 'property_id')
    depth_num = sgqlc.types.Field(Float, graphql_name='depthNum')
    platoon = sgqlc.types.Field(Platoon, graphql_name='platoon')
    position = sgqlc.types.Field(String, graphql_name='position')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class DeleteCurrentClubDepthChartInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'delete_current_club_depth_chart')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    delete_current_club_depth_chart = sgqlc.types.Field(sgqlc.types.non_null(DeleteCurrentClubDepthChart), graphql_name='deleteCurrentClubDepthChart')


class DeleteCurrentClubRoster(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('person_id', 'property_id')
    person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='personId')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class DeleteCurrentClubRosterInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'delete_current_club_roster')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    delete_current_club_roster = sgqlc.types.Field(sgqlc.types.non_null(DeleteCurrentClubRoster), graphql_name='deleteCurrentClubRoster')


class DeleteDraftPick(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('draft_position', 'draft_round', 'draft_year')
    draft_position = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftPosition')
    draft_round = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftRound')
    draft_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftYear')


class DeleteDraftPickInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'delete_draft_pick', 'delete_draft_picks_by_year')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    delete_draft_pick = sgqlc.types.Field(DeleteDraftPick, graphql_name='deleteDraftPick')
    delete_draft_picks_by_year = sgqlc.types.Field('DeleteDraftPicksByYear', graphql_name='deleteDraftPicksByYear')


class DeleteDraftPicksByYear(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('draft_year',)
    draft_year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='draftYear')


class DeleteGameInsight(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('id', 'label')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    label = sgqlc.types.Field(String, graphql_name='label')


class DeleteGameInsightInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'game_insight')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    game_insight = sgqlc.types.Field(sgqlc.types.non_null(DeleteGameInsight), graphql_name='gameInsight')


class DeleteIdentityProvider(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class DeleteIdentityProviderInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'identity_provider')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    identity_provider = sgqlc.types.Field(sgqlc.types.non_null(DeleteIdentityProvider), graphql_name='identityProvider')


class DeleteInjuryReportInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'injury_report_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    injury_report_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='injuryReportId')


class GenerateSmartID(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('legacy_id', 'smart_id')
    legacy_id = sgqlc.types.Field(String, graphql_name='legacyID')
    smart_id = sgqlc.types.Field(sgqlc.types.non_null(SmartID), graphql_name='smartID')


class GenerateSmartIDInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'generate_smart_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    generate_smart_id = sgqlc.types.Field(sgqlc.types.non_null(GenerateSmartID), graphql_name='generateSmartID')


class HeimdallrInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'heimdallr_request')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    heimdallr_request = sgqlc.types.Field(sgqlc.types.non_null('HeimdallrRequest'), graphql_name='heimdallrRequest')


class HeimdallrRequest(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('body', 'destination_uri', 'source', 'tracking_enabled', 'workflow')
    body = sgqlc.types.Field(String, graphql_name='body')
    destination_uri = sgqlc.types.Field(String, graphql_name='destinationUri')
    source = sgqlc.types.Field(String, graphql_name='source')
    tracking_enabled = sgqlc.types.Field(Boolean, graphql_name='trackingEnabled')
    workflow = sgqlc.types.Field(String, graphql_name='workflow')


class InjuredPlayerInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('display_name', 'headshot_id', 'injuries', 'injury_status', 'player_id', 'position', 'practice_statuses', 'practices')
    display_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayName')
    headshot_id = sgqlc.types.Field(String, graphql_name='headshotId')
    injuries = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='injuries')
    injury_status = sgqlc.types.Field(sgqlc.types.non_null(InjuryStatus), graphql_name='injuryStatus')
    player_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='playerId')
    position = sgqlc.types.Field(String, graphql_name='position')
    practice_statuses = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='practiceStatuses')
    practices = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='practices')


class InsightItemInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('external_id', 'facts', 'picker')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    facts = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='facts')
    picker = sgqlc.types.Field(ItemPicker, graphql_name='picker')


class MusicInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('music_cue_id', 'music_duration_secs', 'music_library_name', 'music_title')
    music_cue_id = sgqlc.types.Field(String, graphql_name='musicCueId')
    music_duration_secs = sgqlc.types.Field(Int, graphql_name='musicDurationSecs')
    music_library_name = sgqlc.types.Field(String, graphql_name='musicLibraryName')
    music_title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='musicTitle')


class PlayId(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'play_id')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')


class RemoveContentInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'id', 'property_id', 'season')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')
    season = sgqlc.types.Field(String, graphql_name='season')


class RemoveKeywordInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'keyword', 'property_id')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    keyword = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='keyword')
    property_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='propertyId')


class SaveCelebration(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('animations', 'celebration_end', 'celebration_id', 'celebration_start', 'event_end', 'event_start', 'event_type', 'status')
    animations = sgqlc.types.Field(sgqlc.types.list_of(AnimationInput), graphql_name='animations')
    celebration_end = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='celebrationEnd')
    celebration_id = sgqlc.types.Field(String, graphql_name='celebrationId')
    celebration_start = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='celebrationStart')
    event_end = sgqlc.types.Field(DateTime, graphql_name='eventEnd')
    event_start = sgqlc.types.Field(DateTime, graphql_name='eventStart')
    event_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='eventType')
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')


class SaveCelebrationInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('celebration', 'client_mutation_id')
    celebration = sgqlc.types.Field(sgqlc.types.non_null(SaveCelebration), graphql_name='celebration')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class SaveGameInsight(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('game_id', 'headline', 'id', 'insight', 'insight_type', 'is_evergreen', 'items', 'label')
    game_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='gameId')
    headline = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='headline')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    insight = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='insight')
    insight_type = sgqlc.types.Field(InsightTemplate, graphql_name='insightType')
    is_evergreen = sgqlc.types.Field(Boolean, graphql_name='isEvergreen')
    items = sgqlc.types.Field(sgqlc.types.list_of(InsightItemInput), graphql_name='items')
    label = sgqlc.types.Field(String, graphql_name='label')


class SaveGameInsightInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'game_insight')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    game_insight = sgqlc.types.Field(sgqlc.types.non_null(SaveGameInsight), graphql_name='gameInsight')


class SaveWeek(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('date_begin', 'date_end', 'id', 'season_id', 'season_type', 'season_value', 'week_order', 'week_type', 'week_value')
    date_begin = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='dateBegin')
    date_end = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='dateEnd')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    season_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='seasonId')
    season_type = sgqlc.types.Field(sgqlc.types.non_null(SeasonType), graphql_name='seasonType')
    season_value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='seasonValue')
    week_order = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='weekOrder')
    week_type = sgqlc.types.Field(sgqlc.types.non_null(WeekType), graphql_name='weekType')
    week_value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='weekValue')


class SaveWeekInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'week')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    week = sgqlc.types.Field(sgqlc.types.non_null(SaveWeek), graphql_name='week')


class SocialInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('label', 'link', 'platform')
    label = sgqlc.types.Field(String, graphql_name='label')
    link = sgqlc.types.Field(String, graphql_name='link')
    platform = sgqlc.types.Field(String, graphql_name='platform')


class StringMapInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(String, graphql_name='key')
    value = sgqlc.types.Field(String, graphql_name='value')


class UpdateEliasProspect(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('arm_length', 'background_image_id', 'birth_city', 'birth_date', 'birth_state', 'bottom_line', 'college_class', 'college_conference', 'college_experience', 'college_jersey_number', 'colleges', 'combine_data', 'current_college', 'display_hint', 'draft_id', 'draft_position', 'draft_projection', 'draft_round', 'draft_year', 'elias_college_id', 'elias_home_country', 'elias_position', 'elias_position_id', 'elias_team_id', 'first_name', 'full_first_name', 'grade', 'grade_rubric', 'hand_size', 'headshot_image_id', 'height', 'high_school', 'home_state', 'hometown', 'id', 'last_name', 'middle_name', 'nfl_comparison', 'overview', 'person_id', 'position', 'position_depth', 'profile_author', 'sources_tell_us', 'strengths', 'suffix', 'video_id', 'weaknesses', 'weight', 'year', 'years_of_eligibility_left')
    arm_length = sgqlc.types.Field(String, graphql_name='armLength')
    background_image_id = sgqlc.types.Field(String, graphql_name='backgroundImageId')
    birth_city = sgqlc.types.Field(String, graphql_name='birthCity')
    birth_date = sgqlc.types.Field(String, graphql_name='birthDate')
    birth_state = sgqlc.types.Field(String, graphql_name='birthState')
    bottom_line = sgqlc.types.Field(String, graphql_name='bottomLine')
    college_class = sgqlc.types.Field(String, graphql_name='collegeClass')
    college_conference = sgqlc.types.Field(String, graphql_name='collegeConference')
    college_experience = sgqlc.types.Field(Int, graphql_name='collegeExperience')
    college_jersey_number = sgqlc.types.Field(String, graphql_name='collegeJerseyNumber')
    colleges = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='colleges')
    combine_data = sgqlc.types.Field(CombineDataInput, graphql_name='combineData')
    current_college = sgqlc.types.Field(String, graphql_name='currentCollege')
    display_hint = sgqlc.types.Field(DisplayHint, graphql_name='displayHint')
    draft_id = sgqlc.types.Field(String, graphql_name='draftId')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_projection = sgqlc.types.Field(String, graphql_name='draftProjection')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    elias_college_id = sgqlc.types.Field(Int, graphql_name='eliasCollegeId')
    elias_home_country = sgqlc.types.Field(String, graphql_name='eliasHomeCountry')
    elias_position = sgqlc.types.Field(String, graphql_name='eliasPosition')
    elias_position_id = sgqlc.types.Field(Int, graphql_name='eliasPositionId')
    elias_team_id = sgqlc.types.Field(Int, graphql_name='eliasTeamId')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    full_first_name = sgqlc.types.Field(String, graphql_name='fullFirstName')
    grade = sgqlc.types.Field(Float, graphql_name='grade')
    grade_rubric = sgqlc.types.Field(String, graphql_name='gradeRubric')
    hand_size = sgqlc.types.Field(String, graphql_name='handSize')
    headshot_image_id = sgqlc.types.Field(String, graphql_name='headshotImageId')
    height = sgqlc.types.Field(String, graphql_name='height')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    home_state = sgqlc.types.Field(String, graphql_name='homeState')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='lastName')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nfl_comparison = sgqlc.types.Field(String, graphql_name='nflComparison')
    overview = sgqlc.types.Field(String, graphql_name='overview')
    person_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='personId')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_depth = sgqlc.types.Field(Int, graphql_name='positionDepth')
    profile_author = sgqlc.types.Field(String, graphql_name='profileAuthor')
    sources_tell_us = sgqlc.types.Field(String, graphql_name='sourcesTellUs')
    strengths = sgqlc.types.Field(String, graphql_name='strengths')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    video_id = sgqlc.types.Field(String, graphql_name='videoId')
    weaknesses = sgqlc.types.Field(String, graphql_name='weaknesses')
    weight = sgqlc.types.Field(String, graphql_name='weight')
    year = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='year')
    years_of_eligibility_left = sgqlc.types.Field(Int, graphql_name='yearsOfEligibilityLeft')


class UpdateEliasProspectInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'elias_prospect')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    elias_prospect = sgqlc.types.Field(sgqlc.types.non_null(UpdateEliasProspect), graphql_name='eliasProspect')


class UpdateFranchise(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('current_background_image_id', 'current_logo_image_id', 'current_team_bio', 'id', 'nfl_shop_url', 'official_website_url', 'owner', 'primary_color', 'secondary_color', 'slug', 'socials')
    current_background_image_id = sgqlc.types.Field(String, graphql_name='currentBackgroundImageId')
    current_logo_image_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='currentLogoImageId')
    current_team_bio = sgqlc.types.Field(String, graphql_name='currentTeamBio')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    nfl_shop_url = sgqlc.types.Field(String, graphql_name='nflShopUrl')
    official_website_url = sgqlc.types.Field(String, graphql_name='officialWebsiteUrl')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    primary_color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='primaryColor')
    secondary_color = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='secondaryColor')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of(SocialInput), graphql_name='socials')


class UpdateFranchiseInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'franchise')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    franchise = sgqlc.types.Field(sgqlc.types.non_null(UpdateFranchise), graphql_name='franchise')


class UpdateGame(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('away_team_id', 'category', 'esb_id', 'game_time', 'gsis_id', 'home_team_id', 'id', 'network_channels', 'radio_links', 'slug', 'territory', 'ticket_url', 'venue_id', 'week_id')
    away_team_id = sgqlc.types.Field(String, graphql_name='awayTeamId')
    category = sgqlc.types.Field(String, graphql_name='category')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    game_time = sgqlc.types.Field(DateTime, graphql_name='gameTime')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    home_team_id = sgqlc.types.Field(String, graphql_name='homeTeamId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    network_channels = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='networkChannels')
    radio_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='radioLinks')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    territory = sgqlc.types.Field(String, graphql_name='territory')
    ticket_url = sgqlc.types.Field(String, graphql_name='ticketUrl')
    venue_id = sgqlc.types.Field(String, graphql_name='venueId')
    week_id = sgqlc.types.Field(String, graphql_name='weekId')


class UpdateGameInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'game')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    game = sgqlc.types.Field(sgqlc.types.non_null(UpdateGame), graphql_name='game')


class UpdatePlayerPerson(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('action_shot', 'bio', 'headshot', 'id', 'nick_name', 'slug', 'socials', 'summary')
    action_shot = sgqlc.types.Field(String, graphql_name='actionShot')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    headshot = sgqlc.types.Field(String, graphql_name='headshot')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of(SocialInput), graphql_name='socials')
    summary = sgqlc.types.Field(String, graphql_name='summary')


class UpdatePlayerPersonInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'player_person')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    player_person = sgqlc.types.Field(sgqlc.types.non_null(UpdatePlayerPerson), graphql_name='playerPerson')


class UpdateTeam(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('id', 'venue_ids')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    venue_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='venueIds')


class UpdateTeamInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'team')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    team = sgqlc.types.Field(sgqlc.types.non_null(UpdateTeam), graphql_name='team')


class UpdateVideo(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'available_to_properties_ids', 'available_to_property_ids', 'caption', 'clip_type', 'content_list_ids', 'description', 'entitlement', 'event_ids', 'event_occurred_date', 'franchise_ids', 'game_ids', 'id', 'image_id', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'person_ids', 'pre_roll_enabled', 'primary_channel', 'publish_state', 'related_play_ids', 'repository', 'season_id', 'season_value', 'series_ids', 'show_ids', 'slug', 'tags', 'title', 'video_asset_id', 'week_id', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    available_to_properties_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertiesIds')
    available_to_property_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='availableToPropertyIds')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    clip_type = sgqlc.types.Field(ClipType, graphql_name='clipType')
    content_list_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contentListIds')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    game_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='gameIds')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')
    pre_roll_enabled = sgqlc.types.Field(Boolean, graphql_name='preRollEnabled')
    primary_channel = sgqlc.types.Field(String, graphql_name='primaryChannel')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    related_play_ids = sgqlc.types.Field(sgqlc.types.list_of(PlayId), graphql_name='relatedPlayIds')
    repository = sgqlc.types.Field(Repository, graphql_name='repository')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    series_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='seriesIds')
    show_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='showIds')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(String, graphql_name='title')
    video_asset_id = sgqlc.types.Field(String, graphql_name='videoAssetId')
    week_id = sgqlc.types.Field(String, graphql_name='weekId')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class UpdateVideoInput(sgqlc.types.Input):
    __schema__ = shield
    __field_names__ = ('client_mutation_id', 'video')
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')
    video = sgqlc.types.Field(sgqlc.types.non_null(UpdateVideo), graphql_name='video')



########################################################################
# Output Objects and Interfaces
########################################################################
class AbstractAsset(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('attribution', 'available_to_properties', 'created_date', 'entitlement', 'external_id', 'id', 'last_modified_date', 'property', 'url')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    available_to_properties = sgqlc.types.Field(sgqlc.types.list_of('Property'), graphql_name='availableToProperties')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    property = sgqlc.types.Field('Property', graphql_name='property')
    url = sgqlc.types.Field(String, graphql_name='url')


class AbstractAuditable(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('created_date', 'last_modified_date')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')


class AbstractContent(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('analytics_id', 'associated_content_lists', 'available_to_properties', 'caption', 'created_date', 'description', 'entitlement', 'events', 'franchises', 'games', 'id', 'last_modified_date', 'last_publish_date', 'original_publish_date', 'origination', 'permalink', 'persons', 'primary_content_list', 'property', 'publish_state', 'season', 'season_value', 'shows', 'slug', 'tags', 'title', 'type', 'workflow_status')
    analytics_id = sgqlc.types.Field(String, graphql_name='analyticsId')
    associated_content_lists = sgqlc.types.Field(sgqlc.types.list_of('ContentList'), graphql_name='associatedContentLists')
    available_to_properties = sgqlc.types.Field(sgqlc.types.list_of('Property'), graphql_name='availableToProperties')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    description = sgqlc.types.Field(String, graphql_name='description')
    entitlement = sgqlc.types.Field(Entitlement, graphql_name='entitlement')
    events = sgqlc.types.Field(sgqlc.types.list_of('Event'), graphql_name='events')
    franchises = sgqlc.types.Field(sgqlc.types.list_of('Franchise'), graphql_name='franchises')
    games = sgqlc.types.Field(sgqlc.types.list_of('Game'), graphql_name='games')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    origination = sgqlc.types.Field(Origination, graphql_name='origination')
    permalink = sgqlc.types.Field(String, graphql_name='permalink')
    persons = sgqlc.types.Field(sgqlc.types.list_of('AbstractPerson'), graphql_name='persons')
    primary_content_list = sgqlc.types.Field('ContentList', graphql_name='primaryContentList')
    property = sgqlc.types.Field('Property', graphql_name='property')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    shows = sgqlc.types.Field(sgqlc.types.list_of('Show'), graphql_name='shows')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    title = sgqlc.types.Field(String, graphql_name='title')
    type = sgqlc.types.Field(String, graphql_name='type')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class AbstractContentConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AbstractContentEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class AbstractContentEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(AbstractContent, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AbstractEntity(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('created_date', 'id', 'last_modified_date')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')


class AbstractEntityConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AbstractEntityEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class AbstractEntityEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(AbstractEntity, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AbstractPerson(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('bio', 'birth_date', 'birth_day', 'birth_month', 'birth_year', 'college_name', 'created_date', 'death_day', 'death_month', 'death_year', 'deceased', 'display_name', 'first_name', 'high_school', 'hometown', 'id', 'last_modified_date', 'last_name', 'middle_name', 'nick_name', 'status', 'suffix', 'summary')
    bio = sgqlc.types.Field(String, graphql_name='bio')
    birth_date = sgqlc.types.Field(Date, graphql_name='birthDate')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    college_name = sgqlc.types.Field(String, graphql_name='collegeName')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    death_day = sgqlc.types.Field(Int, graphql_name='deathDay')
    death_month = sgqlc.types.Field(Int, graphql_name='deathMonth')
    death_year = sgqlc.types.Field(Int, graphql_name='deathYear')
    deceased = sgqlc.types.Field(Boolean, graphql_name='deceased')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    high_school = sgqlc.types.Field(String, graphql_name='highSchool')
    hometown = sgqlc.types.Field(String, graphql_name='hometown')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    middle_name = sgqlc.types.Field(String, graphql_name='middleName')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    status = sgqlc.types.Field(Status, graphql_name='status')
    suffix = sgqlc.types.Field(String, graphql_name='suffix')
    summary = sgqlc.types.Field(String, graphql_name='summary')


class AbstractPublishable(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('created_date', 'id', 'last_modified_date', 'last_publish_date', 'original_publish_date', 'publish_state', 'workflow_status')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    publish_state = sgqlc.types.Field(PublishState, graphql_name='publishState')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class Animation(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('asset_url', 'name', 'static_image_url', 'text', 'tracking_pixel_url')
    asset_url = sgqlc.types.Field(String, graphql_name='assetUrl')
    name = sgqlc.types.Field(String, graphql_name='name')
    static_image_url = sgqlc.types.Field(String, graphql_name='staticImageUrl')
    text = sgqlc.types.Field(String, graphql_name='text')
    tracking_pixel_url = sgqlc.types.Field(String, graphql_name='trackingPixelUrl')


class ArticleConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ArticleEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ArticleEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Article'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AssetsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('audio_asset', 'audio_assets', 'audio_assets_by_ids', 'image_asset', 'image_assets', 'image_assets_by_ids', 'video_asset', 'video_assets', 'video_assets_by_ids')
    audio_asset = sgqlc.types.Field('AudioAsset', graphql_name='audioAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    audio_assets = sgqlc.types.Field('AudioAssetConnection', graphql_name='audioAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    audio_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('AudioAsset'), graphql_name='audioAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    image_asset = sgqlc.types.Field('ImageAsset', graphql_name='imageAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    image_assets = sgqlc.types.Field('ImageAssetConnection', graphql_name='imageAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    image_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ImageAsset'), graphql_name='imageAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    video_asset = sgqlc.types.Field('VideoAsset', graphql_name='videoAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    video_assets = sgqlc.types.Field('VideoAssetConnection', graphql_name='videoAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    video_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('VideoAsset'), graphql_name='videoAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class AudioAssetConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AudioAssetEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class AudioAssetEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('AudioAsset'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AudioConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AudioEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class AudioEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Audio'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class AuthorPersonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AuthorPersonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class AuthorPersonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('AuthorPerson'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class Award(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('description', 'season_id', 'season_value', 'type')
    description = sgqlc.types.Field(String, graphql_name='description')
    season_id = sgqlc.types.Field(String, graphql_name='seasonId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    type = sgqlc.types.Field(String, graphql_name='type')


class BlackList(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('country_code', 'description', 'dma_code', 'identity_provider_id', 'network')
    country_code = sgqlc.types.Field(String, graphql_name='countryCode')
    description = sgqlc.types.Field(String, graphql_name='description')
    dma_code = sgqlc.types.Field(String, graphql_name='dmaCode')
    identity_provider_id = sgqlc.types.Field(String, graphql_name='identityProviderId')
    network = sgqlc.types.Field(String, graphql_name='network')


class BroadcastGame(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('affiliate', 'game_id')
    affiliate = sgqlc.types.Field(String, graphql_name='affiliate')
    game_id = sgqlc.types.Field(String, graphql_name='gameId')


class Celebration(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('animations', 'celebration_end', 'celebration_id', 'celebration_start', 'event_end', 'event_start', 'event_type', 'status')
    animations = sgqlc.types.Field(sgqlc.types.list_of(Animation), graphql_name='animations')
    celebration_end = sgqlc.types.Field(DateTime, graphql_name='celebrationEnd')
    celebration_id = sgqlc.types.Field(String, graphql_name='celebrationId')
    celebration_start = sgqlc.types.Field(DateTime, graphql_name='celebrationStart')
    event_end = sgqlc.types.Field(DateTime, graphql_name='eventEnd')
    event_start = sgqlc.types.Field(DateTime, graphql_name='eventStart')
    event_type = sgqlc.types.Field(String, graphql_name='eventType')
    status = sgqlc.types.Field(String, graphql_name='status')


class CheerleaderConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CheerleaderEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class CheerleaderEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Cheerleader'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CheerleaderPersonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CheerleaderPersonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class CheerleaderPersonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('CheerleaderPerson'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ClubTransactionConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ClubTransactionEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ClubTransactionEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ClubTransaction'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ClubsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('club_injury_reports', 'club_transaction', 'club_transactions', 'club_transactions_by_ids', 'current_club_depth_chart', 'current_club_roster', 'depth_chart_position_order', 'injury_report', 'injury_reports', 'injury_reports_by_ids')
    club_injury_reports = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('ClubInjury')), graphql_name='clubInjuryReports', args=sgqlc.types.ArgDict((
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
        ('season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='seasonValue', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('week_value', sgqlc.types.Arg(Int, graphql_name='weekValue', default=None)),
))
    )
    club_transaction = sgqlc.types.Field('ClubTransaction', graphql_name='clubTransaction', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    club_transactions = sgqlc.types.Field(ClubTransactionConnection, graphql_name='clubTransactions', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(TransactionOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('transaction_year', sgqlc.types.Arg(Int, graphql_name='transactionYear', default=None)),
        ('franchise_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise_id', default=None)),
))
    )
    club_transactions_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ClubTransaction'), graphql_name='clubTransactionsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    current_club_depth_chart = sgqlc.types.Field(sgqlc.types.list_of('CurrentClubDepthChart'), graphql_name='currentClubDepthChart', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
))
    )
    current_club_roster = sgqlc.types.Field(sgqlc.types.list_of('CurrentClubRoster'), graphql_name='currentClubRoster', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
))
    )
    depth_chart_position_order = sgqlc.types.Field('DepthChartPositionOrder', graphql_name='depthChartPositionOrder', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
))
    )
    injury_report = sgqlc.types.Field('Injury', graphql_name='injuryReport', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    injury_reports = sgqlc.types.Field('InjuryConnection', graphql_name='injuryReports', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(InjuryReportOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
        ('team_abbreviation', sgqlc.types.Arg(String, graphql_name='team_abbreviation', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
))
    )
    injury_reports_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Injury'), graphql_name='injuryReportsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class CoachConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CoachEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class CoachEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Coach'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CoachPersonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CoachPersonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class CoachPersonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('CoachPerson'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class CombineData(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('bench_result', 'bench_result_video_ids', 'broad_jump_result', 'broad_jump_result_video_ids', 'combine_number', 'forty_yard_dash_result', 'forty_yard_dash_result_is_official', 'forty_yard_dash_result_video_ids', 'sixty_yard_shuttle_result', 'sixty_yard_shuttle_result_video_ids', 'three_cone_drill_result', 'three_cone_drill_result_video_ids', 'twenty_yard_shuttle_result', 'twenty_yard_shuttle_result_video_ids', 'vertical_jump_result', 'vertical_jump_result_video_ids')
    bench_result = sgqlc.types.Field(String, graphql_name='benchResult')
    bench_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='benchResultVideoIds')
    broad_jump_result = sgqlc.types.Field(String, graphql_name='broadJumpResult')
    broad_jump_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='broadJumpResultVideoIds')
    combine_number = sgqlc.types.Field(String, graphql_name='combineNumber')
    forty_yard_dash_result = sgqlc.types.Field(String, graphql_name='fortyYardDashResult')
    forty_yard_dash_result_is_official = sgqlc.types.Field(Boolean, graphql_name='fortyYardDashResultIsOfficial')
    forty_yard_dash_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fortyYardDashResultVideoIds')
    sixty_yard_shuttle_result = sgqlc.types.Field(String, graphql_name='sixtyYardShuttleResult')
    sixty_yard_shuttle_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='sixtyYardShuttleResultVideoIds')
    three_cone_drill_result = sgqlc.types.Field(String, graphql_name='threeConeDrillResult')
    three_cone_drill_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='threeConeDrillResultVideoIds')
    twenty_yard_shuttle_result = sgqlc.types.Field(String, graphql_name='twentyYardShuttleResult')
    twenty_yard_shuttle_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='twentyYardShuttleResultVideoIds')
    vertical_jump_result = sgqlc.types.Field(String, graphql_name='verticalJumpResult')
    vertical_jump_result_video_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='verticalJumpResultVideoIds')


class ContentGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('article', 'articles', 'articles_by_ids', 'audio', 'audios', 'audios_by_ids', 'content_list', 'content_list_by_tag', 'content_lists', 'content_lists_by_ids', 'content_lists_by_tags', 'event', 'events', 'events_by_ids', 'image', 'images', 'images_by_ids', 'mock_draft', 'mock_draft_pick', 'mock_draft_picks', 'mock_draft_picks_by_ids', 'mock_drafts', 'mock_drafts_by_ids', 'person_list', 'person_list_by_tag', 'person_lists', 'person_lists_by_ids', 'promo', 'promos', 'promos_by_ids', 'properties', 'properties_by_ids', 'property', 'series', 'series_list', 'series_list_by_ids', 'tag', 'tags', 'tags_by_ids', 'video', 'videos', 'videos_by_ids')
    article = sgqlc.types.Field('Article', graphql_name='article', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    articles = sgqlc.types.Field(ArticleConnection, graphql_name='articles', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('events_id', sgqlc.types.Arg(String, graphql_name='events_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    articles_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Article'), graphql_name='articlesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    audio = sgqlc.types.Field('Audio', graphql_name='audio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    audios = sgqlc.types.Field(AudioConnection, graphql_name='audios', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('events_id', sgqlc.types.Arg(String, graphql_name='events_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    audios_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Audio'), graphql_name='audiosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    content_list = sgqlc.types.Field('ContentList', graphql_name='contentList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    content_list_by_tag = sgqlc.types.Field('ContentList', graphql_name='contentListByTag', args=sgqlc.types.ArgDict((
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    content_lists = sgqlc.types.Field('ContentListConnection', graphql_name='contentLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('content_hints', sgqlc.types.Arg(ContentHint, graphql_name='contentHints', default=None)),
        ('content_list_type', sgqlc.types.Arg(ContentHint, graphql_name='contentListType', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('external_id', sgqlc.types.Arg(String, graphql_name='externalId', default=None)),
))
    )
    content_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ContentList'), graphql_name='contentListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    content_lists_by_tags = sgqlc.types.Field(sgqlc.types.list_of('ContentList'), graphql_name='contentListsByTags', args=sgqlc.types.ArgDict((
        ('tags', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='tags', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    event = sgqlc.types.Field('Event', graphql_name='event', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    events = sgqlc.types.Field('EventConnection', graphql_name='events', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('start_date', sgqlc.types.Arg(String, graphql_name='startDate', default=None)),
        ('end_date', sgqlc.types.Arg(String, graphql_name='endDate', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
))
    )
    events_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Event'), graphql_name='eventsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    image = sgqlc.types.Field('Image', graphql_name='image', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    images = sgqlc.types.Field('ImageConnection', graphql_name='images', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('events_id', sgqlc.types.Arg(String, graphql_name='events_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    images_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Image'), graphql_name='imagesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    mock_draft = sgqlc.types.Field('MockDraft', graphql_name='mockDraft', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    mock_draft_pick = sgqlc.types.Field('MockDraftPick', graphql_name='mockDraftPick', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    mock_draft_picks = sgqlc.types.Field('MockDraftPickConnection', graphql_name='mockDraftPicks', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(MockDraftPickOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('franchise_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise_id', default=None)),
        ('prospect_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='prospect_id', default=None)),
        ('pick_number', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='pickNumber', default=None)),
))
    )
    mock_draft_picks_by_ids = sgqlc.types.Field(sgqlc.types.list_of('MockDraftPick'), graphql_name='mockDraftPicksByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    mock_drafts = sgqlc.types.Field('MockDraftConnection', graphql_name='mockDrafts', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(MockDraftOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('author_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='author_id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='version', default=None)),
        ('year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='year', default=None)),
))
    )
    mock_drafts_by_ids = sgqlc.types.Field(sgqlc.types.list_of('MockDraft'), graphql_name='mockDraftsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    person_list = sgqlc.types.Field('PersonList', graphql_name='personList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    person_list_by_tag = sgqlc.types.Field('PersonList', graphql_name='personListByTag', args=sgqlc.types.ArgDict((
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    person_lists = sgqlc.types.Field('PersonListConnection', graphql_name='personLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
))
    )
    person_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PersonList'), graphql_name='personListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    promo = sgqlc.types.Field('Promo', graphql_name='promo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    promos = sgqlc.types.Field('PromoConnection', graphql_name='promos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    promos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Promo'), graphql_name='promosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    properties = sgqlc.types.Field('PropertyConnection', graphql_name='properties', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PropertyOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_type', sgqlc.types.Arg(PropertyType, graphql_name='propertyType', default=None)),
        ('enabled', sgqlc.types.Arg(Boolean, graphql_name='enabled', default=None)),
))
    )
    properties_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Property'), graphql_name='propertiesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    property = sgqlc.types.Field('Property', graphql_name='property', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    series = sgqlc.types.Field('Series', graphql_name='series', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    series_list = sgqlc.types.Field('SeriesConnection', graphql_name='seriesList', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
))
    )
    series_list_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Series'), graphql_name='seriesListByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    tag = sgqlc.types.Field('Tag', graphql_name='tag', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    tags_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tagsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    video = sgqlc.types.Field('Video', graphql_name='video', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    videos = sgqlc.types.Field('VideoConnection', graphql_name='videos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ContentOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('last_modified_date_daterange', sgqlc.types.Arg(String, graphql_name='lastModifiedDateDATERANGE', default=None)),
        ('original_publish_date_daterange', sgqlc.types.Arg(String, graphql_name='originalPublishDateDATERANGE', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('events_id', sgqlc.types.Arg(String, graphql_name='events_id', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('week_season_value', sgqlc.types.Arg(Int, graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('related_play_ids_play_id', sgqlc.types.Arg(Int, graphql_name='relatedPlayIds_playId', default=None)),
        ('related_play_ids_game_detail_id', sgqlc.types.Arg(String, graphql_name='relatedPlayIds_gameDetailId', default=None)),
        ('clip_type', sgqlc.types.Arg(ClipType, graphql_name='clipType', default=None)),
        ('primary_channel', sgqlc.types.Arg(String, graphql_name='primaryChannel', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('slug', sgqlc.types.Arg(String, graphql_name='slug', default=None)),
        ('video_asset_id_exists', sgqlc.types.Arg(Existence, graphql_name='videoAsset_idEXISTS', default=None)),
))
    )
    videos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Video'), graphql_name='videosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class ContentListConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ContentListEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ContentListEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ContentList'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class DraftConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('DraftEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class DraftEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Draft'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class DraftPick(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('analysis', 'created_date', 'draft_number_overall', 'draft_player_position', 'draft_position', 'draft_round', 'draft_team', 'draft_type', 'draft_year', 'franchise_id', 'last_modified_date', 'pick_is_in', 'player', 'prospect', 'trade_note')
    analysis = sgqlc.types.Field(String, graphql_name='analysis')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    draft_number_overall = sgqlc.types.Field(Int, graphql_name='draftNumberOverall')
    draft_player_position = sgqlc.types.Field(String, graphql_name='draftPlayerPosition')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_team = sgqlc.types.Field('DraftTeam', graphql_name='draftTeam')
    draft_type = sgqlc.types.Field(String, graphql_name='draftType')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    franchise_id = sgqlc.types.Field(String, graphql_name='franchiseId')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    pick_is_in = sgqlc.types.Field(Boolean, graphql_name='pickIsIn')
    player = sgqlc.types.Field('Player', graphql_name='player')
    prospect = sgqlc.types.Field('Prospect', graphql_name='prospect')
    trade_note = sgqlc.types.Field(String, graphql_name='tradeNote')


class DraftTeamConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('DraftTeamEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class DraftTeamEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('DraftTeam'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class EliasCountry(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('code', 'description')
    code = sgqlc.types.Field(String, graphql_name='code')
    description = sgqlc.types.Field(String, graphql_name='description')


class EliasGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('colleges', 'countries', 'positions', 'teams')
    colleges = sgqlc.types.Field(sgqlc.types.list_of('EliasCollege'), graphql_name='colleges')
    countries = sgqlc.types.Field(sgqlc.types.list_of(EliasCountry), graphql_name='countries')
    positions = sgqlc.types.Field(sgqlc.types.list_of('EliasPosition'), graphql_name='positions')
    teams = sgqlc.types.Field(sgqlc.types.list_of('EliasTeam'), graphql_name='teams', args=sgqlc.types.ArgDict((
        ('season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season', default=None)),
))
    )


class EliasPageInfo(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('next_page',)
    next_page = sgqlc.types.Field(String, graphql_name='nextPage')


class EliasPlayerGameStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasPlayerGameStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasPlayerGameStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null('EliasPlayerGameStats'), graphql_name='node')


class EliasPlayerSplitStats(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'person', 'person_split_stats', 'player', 'season_value', 'split_category', 'split_subcategory', 'team')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    person_split_stats = sgqlc.types.Field('EliasStatsDetail', graphql_name='personSplitStats')
    player = sgqlc.types.Field('Player', graphql_name='player')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    split_category = sgqlc.types.Field(SplitCategory, graphql_name='splitCategory')
    split_subcategory = sgqlc.types.Field(String, graphql_name='splitSubcategory')
    team = sgqlc.types.Field('Team', graphql_name='team')


class EliasPlayerSplitStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasPlayerSplitStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasPlayerSplitStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null(EliasPlayerSplitStats), graphql_name='node')


class EliasPlayerTeamStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasPlayerTeamStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasPlayerTeamStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null('EliasPlayerTeamStats'), graphql_name='node')


class EliasPlayerTeamStatsRank(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('person', 'person_team_stats', 'rank', 'season_type')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    person_team_stats = sgqlc.types.Field('EliasStatsDetail', graphql_name='personTeamStats')
    rank = sgqlc.types.Field(Int, graphql_name='rank')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')


class EliasPlayerTeamStatsTop(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('person', 'person_team_stats', 'player', 'rank', 'season_type', 'season_value')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    person_team_stats = sgqlc.types.Field('EliasStatsDetail', graphql_name='personTeamStats')
    player = sgqlc.types.Field('Player', graphql_name='player')
    rank = sgqlc.types.Field(Int, graphql_name='rank')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')


class EliasPlayerTeamStatsTopConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasPlayerTeamStatsTopEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasPlayerTeamStatsTopEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null(EliasPlayerTeamStatsTop), graphql_name='node')


class EliasStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_tackles_for_aloss', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'first_downs_per_game_average', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made1_to19_pct', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made20_to29_pct', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made30_to39_pct', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made40_to49_pct', 'kicking_fg_att_made50plus', 'kicking_fg_att_made50plus_pct', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_attempts_per_game_average', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_completions_per_game_average', 'passing_first_down_percentage', 'passing_first_downs', 'passing_first_downs_per_game_average', 'passing_fumbles', 'passing_interception_percentage', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_touchdowns_to_interceptions', 'passing_yards', 'passing_yards_per_game_average', 'penalties_total', 'penalties_yards_penalized', 'points_per_game_average', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percentage', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'receiving_yards_per_game_average', 'receiving_yards_to_receptions', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_attempts_per_game_average', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'rushing_yards_per_game_average', 'scrimmage_plays', 'scrimmage_yds', 'start_position', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'time_of_poss_seconds_per_game_average', 'total_points_scored', 'total_points_scored_per_game_average', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total', 'turnover_differential', 'yards_per_game_average')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_tackles_for_aloss = sgqlc.types.Field(Float, graphql_name='defensiveTacklesForALoss')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    first_downs_per_game_average = sgqlc.types.Field(Float, graphql_name='firstDownsPerGameAverage')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made1_to19_pct = sgqlc.types.Field(Float, graphql_name='kickingFgAttMade1To19Pct')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made20_to29_pct = sgqlc.types.Field(Float, graphql_name='kickingFgAttMade20To29Pct')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made30_to39_pct = sgqlc.types.Field(Float, graphql_name='kickingFgAttMade30To39Pct')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made40_to49_pct = sgqlc.types.Field(Float, graphql_name='kickingFgAttMade40To49Pct')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_att_made50plus_pct = sgqlc.types.Field(Float, graphql_name='kickingFgAttMade50plusPct')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_attempts_per_game_average = sgqlc.types.Field(Float, graphql_name='passingAttemptsPerGameAverage')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_completions_per_game_average = sgqlc.types.Field(Float, graphql_name='passingCompletionsPerGameAverage')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_first_downs_per_game_average = sgqlc.types.Field(Float, graphql_name='passingFirstDownsPerGameAverage')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percentage = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercentage')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_touchdowns_to_interceptions = sgqlc.types.Field(String, graphql_name='passingTouchdownsToInterceptions')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    passing_yards_per_game_average = sgqlc.types.Field(Float, graphql_name='passingYardsPerGameAverage')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    points_per_game_average = sgqlc.types.Field(Float, graphql_name='pointsPerGameAverage')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percentage = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercentage')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    receiving_yards_per_game_average = sgqlc.types.Field(Float, graphql_name='receivingYardsPerGameAverage')
    receiving_yards_to_receptions = sgqlc.types.Field(String, graphql_name='receivingYardsToReceptions')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_attempts_per_game_average = sgqlc.types.Field(Float, graphql_name='rushingAttemptsPerGameAverage')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    rushing_yards_per_game_average = sgqlc.types.Field(Float, graphql_name='rushingYardsPerGameAverage')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    start_position = sgqlc.types.Field(String, graphql_name='startPosition')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    time_of_poss_seconds_per_game_average = sgqlc.types.Field(Float, graphql_name='timeOfPossSecondsPerGameAverage')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    total_points_scored_per_game_average = sgqlc.types.Field(Float, graphql_name='totalPointsScoredPerGameAverage')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')
    turnover_differential = sgqlc.types.Field(Float, graphql_name='turnoverDifferential')
    yards_per_game_average = sgqlc.types.Field(Float, graphql_name='yardsPerGameAverage')


class EliasStatsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('person_split_stat', 'person_split_stats', 'player_game_stats', 'player_team_stats', 'player_team_stats_rank', 'player_team_stats_top', 'team_game_stats', 'team_split_stat', 'team_split_stats', 'team_stat', 'team_stats', 'team_stats_top')
    person_split_stat = sgqlc.types.Field(EliasPlayerSplitStats, graphql_name='personSplitStat', args=sgqlc.types.ArgDict((
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('person_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='personId', default=None)),
        ('split_category', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='splitCategory', default=None)),
        ('split_sub_category', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='splitSubCategory', default=None)),
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
))
    )
    person_split_stats = sgqlc.types.Field(EliasPlayerSplitStatsConnection, graphql_name='personSplitStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('person_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='personId', default=None)),
))
    )
    player_game_stats = sgqlc.types.Field(EliasPlayerGameStatsConnection, graphql_name='playerGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='playerId', default=None)),
        ('season', sgqlc.types.Arg(Int, graphql_name='season', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='gameId', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
))
    )
    player_team_stats = sgqlc.types.Field(EliasPlayerTeamStatsConnection, graphql_name='playerTeamStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='playerId', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
))
    )
    player_team_stats_rank = sgqlc.types.Field(EliasPlayerTeamStatsRank, graphql_name='playerTeamStatsRank', args=sgqlc.types.ArgDict((
        ('order_by', sgqlc.types.Arg(sgqlc.types.non_null(EliasStatsLeadersOrderBy), graphql_name='orderBy', default=None)),
        ('person_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='personId', default=None)),
        ('season', sgqlc.types.Arg(Int, graphql_name='season', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    player_team_stats_top = sgqlc.types.Field(EliasPlayerTeamStatsTopConnection, graphql_name='playerTeamStatsTop', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.non_null(EliasStatsLeadersOrderBy), graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season', sgqlc.types.Arg(Int, graphql_name='season', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
        ('player_position', sgqlc.types.Arg(Position, graphql_name='playerPosition', default=None)),
        ('position_group', sgqlc.types.Arg(PositionGroup, graphql_name='positionGroup', default=None)),
))
    )
    team_game_stats = sgqlc.types.Field(EliasPlayerTeamStatsConnection, graphql_name='teamGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='gameId', default=None)),
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
))
    )
    team_split_stat = sgqlc.types.Field('EliasTeamSplitStats', graphql_name='teamSplitStat', args=sgqlc.types.ArgDict((
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('split_category', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='splitCategory', default=None)),
        ('split_sub_category', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='splitSubCategory', default=None)),
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
))
    )
    team_split_stats = sgqlc.types.Field('EliasTeamSplitStatsConnection', graphql_name='teamSplitStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
))
    )
    team_stat = sgqlc.types.Field('EliasTeamStats', graphql_name='teamStat', args=sgqlc.types.ArgDict((
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='teamId', default=None)),
))
    )
    team_stats = sgqlc.types.Field('EliasTeamStatsConnection', graphql_name='teamStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    team_stats_top = sgqlc.types.Field('EliasTeamStatsTopConnection', graphql_name='teamStatsTop', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('next', sgqlc.types.Arg(String, graphql_name='next', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.non_null(EliasStatsLeadersOrderBy), graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season', sgqlc.types.Arg(Int, graphql_name='season', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('role', sgqlc.types.Arg(StatsRole, graphql_name='role', default=None)),
))
    )


class EliasTeamSplitStats(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'person', 'season_type', 'season_value', 'split_category', 'split_subcategory', 'team', 'team_split_stats')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    split_category = sgqlc.types.Field(String, graphql_name='splitCategory')
    split_subcategory = sgqlc.types.Field(String, graphql_name='splitSubcategory')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_split_stats = sgqlc.types.Field(EliasStatsDetail, graphql_name='teamSplitStats')


class EliasTeamSplitStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasTeamSplitStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasTeamSplitStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null(EliasTeamSplitStats), graphql_name='node')


class EliasTeamStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasTeamStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasTeamStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null('EliasTeamStats'), graphql_name='node')


class EliasTeamStatsTop(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'rank', 'season_type', 'season_value', 'team', 'team_stats')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    rank = sgqlc.types.Field(Int, graphql_name='rank')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_stats = sgqlc.types.Field(EliasStatsDetail, graphql_name='teamStats')


class EliasTeamStatsTopConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EliasTeamStatsTopEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(EliasPageInfo), graphql_name='pageInfo')


class EliasTeamStatsTopEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node',)
    node = sgqlc.types.Field(sgqlc.types.non_null(EliasTeamStatsTop), graphql_name='node')


class EventConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('EventEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class EventEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Event'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class EventRadiusInfo(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('event_ids', 'geo_in_radius', 'venue')
    event_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='eventIds')
    geo_in_radius = sgqlc.types.Field(Boolean, graphql_name='geoInRadius')
    venue = sgqlc.types.Field(String, graphql_name='venue')


class ExecutiveConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ExecutiveEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ExecutiveEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Executive'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ExecutivePersonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ExecutivePersonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ExecutivePersonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ExecutivePerson'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class FantasyCelebrationGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('celebration', 'celebrations')
    celebration = sgqlc.types.Field(Celebration, graphql_name='celebration', args=sgqlc.types.ArgDict((
        ('celebration_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='celebrationId', default=None)),
))
    )
    celebrations = sgqlc.types.Field(sgqlc.types.list_of(Celebration), graphql_name='celebrations', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(String, graphql_name='filter', default=None)),
))
    )


class FavoriteTeams(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('country_code', 'franchise_ids', 'postal_code')
    country_code = sgqlc.types.Field(String, graphql_name='countryCode')
    franchise_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='franchiseIds')
    postal_code = sgqlc.types.Field(String, graphql_name='postalCode')


class FranchiseConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('FranchiseEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class FranchiseEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Franchise'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class FranchiseInjuryMs(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'persons')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    persons = sgqlc.types.Field(sgqlc.types.list_of('InjuredPersonMs'), graphql_name='persons')


class FranchiseToPropertyPayload(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'property')
    franchise = sgqlc.types.Field(String, graphql_name='franchise')
    property = sgqlc.types.Field(String, graphql_name='property')


class GameConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GameEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class GameEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Game'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class GameInjuryMs(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('away_franchise', 'game', 'home_franchise')
    away_franchise = sgqlc.types.Field(FranchiseInjuryMs, graphql_name='awayFranchise')
    game = sgqlc.types.Field('Game', graphql_name='game')
    home_franchise = sgqlc.types.Field(FranchiseInjuryMs, graphql_name='homeFranchise')


class GameInjuryMsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GameInjuryMsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class GameInjuryMsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null(GameInjuryMs), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class GameInsightConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('GameInsightEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class GameInsightEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field('GameInsight', graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class GameInsightGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('insight_by_id', 'insights', 'insights_by_game', 'insights_by_games')
    insight_by_id = sgqlc.types.Field('GameInsight', graphql_name='insightById', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('label', sgqlc.types.Arg(String, graphql_name='label', default='')),
))
    )
    insights = sgqlc.types.Field(GameInsightConnection, graphql_name='insights', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='playerId', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
        ('insight_type', sgqlc.types.Arg(InsightTemplate, graphql_name='insightType', default=None)),
        ('is_evergreen', sgqlc.types.Arg(Boolean, graphql_name='isEvergreen', default=True)),
))
    )
    insights_by_game = sgqlc.types.Field(sgqlc.types.list_of('GameInsight'), graphql_name='insightsByGame', args=sgqlc.types.ArgDict((
        ('game_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameId', default=None)),
        ('label', sgqlc.types.Arg(String, graphql_name='label', default='')),
))
    )
    insights_by_games = sgqlc.types.Field(sgqlc.types.list_of('GameInsight'), graphql_name='insightsByGames', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class GeneratedSmartID(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('uuid',)
    uuid = sgqlc.types.Field(String, graphql_name='uuid')


class HeimdallrResponse(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('error_message', 'process_time', 'status', 'ticket_id', 'workflow_name')
    error_message = sgqlc.types.Field(String, graphql_name='errorMessage')
    process_time = sgqlc.types.Field(Int, graphql_name='processTime')
    status = sgqlc.types.Field(String, graphql_name='status')
    ticket_id = sgqlc.types.Field(String, graphql_name='ticketId')
    workflow_name = sgqlc.types.Field(String, graphql_name='workflowName')


class ImageAssetConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ImageAssetEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ImageAssetEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ImageAsset'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ImageConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ImageEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class ImageEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Image'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class InjuredPersonMs(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('display_name', 'injuries', 'injury_status', 'person', 'position', 'practice_status', 'practices')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='injuries')
    injury_status = sgqlc.types.Field(String, graphql_name='injuryStatus')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    position = sgqlc.types.Field(Position, graphql_name='position')
    practice_status = sgqlc.types.Field(String, graphql_name='practiceStatus')
    practices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practices')


class InjuryConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('InjuryEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class InjuryEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Injury'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class InsightItem(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('external_id', 'facts', 'picker', 'player', 'player_id', 'team', 'team_id')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    facts = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='facts')
    picker = sgqlc.types.Field(ItemPicker, graphql_name='picker')
    player = sgqlc.types.Field('Player', graphql_name='player')
    player_id = sgqlc.types.Field(String, graphql_name='playerId')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')


class Key(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('count', 'name')
    count = sgqlc.types.Field(Long, graphql_name='count')
    name = sgqlc.types.Field(String, graphql_name='name')


class KeyValue(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('keyword', 'metadata', 'url')
    keyword = sgqlc.types.Field(String, graphql_name='keyword')
    metadata = sgqlc.types.Field(Map, graphql_name='metadata')
    url = sgqlc.types.Field(String, graphql_name='url')


class KeycountResponse(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('time_series_counts', 'total_counts')
    time_series_counts = sgqlc.types.Field(sgqlc.types.list_of('TimeSeriesCount'), graphql_name='timeSeriesCounts')
    total_counts = sgqlc.types.Field(sgqlc.types.list_of('TotalCount'), graphql_name='totalCounts')


class LeagueGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('current', 'current_contextual', 'draft', 'draft_by_year', 'draft_picks', 'draft_team', 'draft_teams', 'draft_teams_by_ids', 'drafts_by_ids', 'drive', 'drives', 'game', 'game_detail', 'game_details_by_ids', 'games', 'games_by_ids', 'games_by_week', 'league_injury_reports_by_team', 'league_injury_reports_by_week', 'league_transactions', 'milestone_players', 'milestone_teams', 'play', 'play_stats', 'plays', 'previous_match_ups', 'season', 'seasons')
    current = sgqlc.types.Field('Current', graphql_name='current', args=sgqlc.types.ArgDict((
        ('date', sgqlc.types.Arg(DateTime, graphql_name='date', default=None)),
))
    )
    current_contextual = sgqlc.types.Field(sgqlc.types.list_of('CurrentContextual'), graphql_name='currentContextual', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(CurrentType, graphql_name='type', default=None)),
        ('context', sgqlc.types.Arg(CurrentContext, graphql_name='context', default=None)),
))
    )
    draft = sgqlc.types.Field('Draft', graphql_name='draft', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    draft_by_year = sgqlc.types.Field('Draft', graphql_name='draftByYear', args=sgqlc.types.ArgDict((
        ('year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='year', default=None)),
))
    )
    draft_picks = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(DraftPick)), graphql_name='draftPicks', args=sgqlc.types.ArgDict((
        ('draft_year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='draftYear', default=None)),
        ('draft_round', sgqlc.types.Arg(Int, graphql_name='draftRound', default=None)),
        ('draft_position', sgqlc.types.Arg(Int, graphql_name='draftPosition', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
        ('order_by', sgqlc.types.Arg(DraftPickOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
))
    )
    draft_team = sgqlc.types.Field('DraftTeam', graphql_name='draftTeam', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    draft_teams = sgqlc.types.Field(DraftTeamConnection, graphql_name='draftTeams', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(YearOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('year', sgqlc.types.Arg(Int, graphql_name='year', default=None)),
))
    )
    draft_teams_by_ids = sgqlc.types.Field(sgqlc.types.list_of('DraftTeam'), graphql_name='draftTeamsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    drafts_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Draft'), graphql_name='draftsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    drive = sgqlc.types.Field(sgqlc.types.non_null('Drive'), graphql_name='drive', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
        ('order_sequence', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='orderSequence', default=None)),
))
    )
    drives = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Drive')), graphql_name='drives', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
))
    )
    game = sgqlc.types.Field('Game', graphql_name='game', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    game_detail = sgqlc.types.Field('GameDetail', graphql_name='gameDetail', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    game_details_by_ids = sgqlc.types.Field(sgqlc.types.list_of('GameDetail'), graphql_name='gameDetailsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    games = sgqlc.types.Field(GameConnection, graphql_name='games', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(GameOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('gsis_id', sgqlc.types.Arg(Int, graphql_name='gsisId', default=None)),
        ('esb_id', sgqlc.types.Arg(Int, graphql_name='esbId', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    games_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Game'), graphql_name='gamesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    games_by_week = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Game')), graphql_name='gamesByWeek', args=sgqlc.types.ArgDict((
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_weekValue', default=None)),
))
    )
    league_injury_reports_by_team = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('LeagueInjury')), graphql_name='leagueInjuryReportsByTeam', args=sgqlc.types.ArgDict((
        ('franchise_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchiseId', default=None)),
        ('season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season', default=None)),
))
    )
    league_injury_reports_by_week = sgqlc.types.Field(GameInjuryMsConnection, graphql_name='leagueInjuryReportsByWeek', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='seasonValue', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('week_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='weekValue', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    league_transactions = sgqlc.types.Field('LeagueTransactionConnection', graphql_name='leagueTransactions', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='year', default=None)),
        ('month', sgqlc.types.Arg(Int, graphql_name='month', default=None)),
        ('transaction_type', sgqlc.types.Arg(String, graphql_name='transactionType', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    milestone_players = sgqlc.types.Field(sgqlc.types.list_of('MilestonePlayer'), graphql_name='milestonePlayers', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
))
    )
    milestone_teams = sgqlc.types.Field(sgqlc.types.list_of('MilestoneTeam'), graphql_name='milestoneTeams', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
))
    )
    play = sgqlc.types.Field('Play', graphql_name='play', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
        ('play_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='playId', default=None)),
))
    )
    play_stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('PlayStats')), graphql_name='playStats', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
        ('play_id', sgqlc.types.Arg(Int, graphql_name='playId', default=None)),
))
    )
    plays = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Play')), graphql_name='plays', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
))
    )
    previous_match_ups = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Game')), graphql_name='previousMatchUps', args=sgqlc.types.ArgDict((
        ('franchise1', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise1', default=None)),
        ('franchise2', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise2', default=None)),
        ('from_season', sgqlc.types.Arg(Int, graphql_name='fromSeason', default=None)),
        ('to_season', sgqlc.types.Arg(Int, graphql_name='toSeason', default=None)),
))
    )
    season = sgqlc.types.Field('Season', graphql_name='season', args=sgqlc.types.ArgDict((
        ('season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season', default=None)),
))
    )
    seasons = sgqlc.types.Field('SeasonConnection', graphql_name='seasons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
))
    )


class LeagueInjury(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('display_name', 'injuries', 'injury_status', 'person', 'position', 'practice_status', 'practices', 'season', 'season_type', 'week')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='injuries')
    injury_status = sgqlc.types.Field(String, graphql_name='injuryStatus')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    position = sgqlc.types.Field(String, graphql_name='position')
    practice_status = sgqlc.types.Field(String, graphql_name='practiceStatus')
    practices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practices')
    season = sgqlc.types.Field(Int, graphql_name='season')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    week = sgqlc.types.Field(Int, graphql_name='week')


class LeagueTransactionConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('LeagueTransactionEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class LeagueTransactionEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('LeagueTransaction'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class LegacyIdInfo(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('type', 'value')
    type = sgqlc.types.Field(LegacyId, graphql_name='type')
    value = sgqlc.types.Field(String, graphql_name='value')


class LiveGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('player_game_stats', 'team_game_stats')
    player_game_stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('LivePlayerGameStats')), graphql_name='playerGameStats', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
        ('gsis_player_id', sgqlc.types.Arg(String, graphql_name='gsisPlayerId', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    team_game_stats = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('LiveTeamGameStats')), graphql_name='teamGameStats', args=sgqlc.types.ArgDict((
        ('game_detail_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gameDetailId', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='teamId', default=None)),
))
    )


class Media(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('playback_url',)
    playback_url = sgqlc.types.Field(String, graphql_name='playbackUrl')


class Meta(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('entity_id', 'entity_type', 'key', 'property_id', 'value')
    entity_id = sgqlc.types.Field(String, graphql_name='entityId')
    entity_type = sgqlc.types.Field(String, graphql_name='entityType')
    key = sgqlc.types.Field(String, graphql_name='key')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    value = sgqlc.types.Field(String, graphql_name='value')


class MilestonePlayer(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'game_detail_id', 'gsis_player_id', 'milestone_type', 'milestone_value', 'person', 'play_id', 'player_game_stats', 'team')
    current_team_id = sgqlc.types.Field(String, graphql_name='currentTeamId')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    gsis_player_id = sgqlc.types.Field(String, graphql_name='gsisPlayerId')
    milestone_type = sgqlc.types.Field(MilestoneType, graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(Int, graphql_name='milestoneValue')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')
    player_game_stats = sgqlc.types.Field('LivePlayerGameStats', graphql_name='playerGameStats')
    team = sgqlc.types.Field('Team', graphql_name='team')


class MockDraftConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MockDraftEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class MockDraftEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('MockDraft'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class MockDraftPickConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MockDraftPickEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfoWithTotal'), graphql_name='pageInfo')


class MockDraftPickEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('MockDraftPick'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class Music(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('music_cue_id', 'music_duration_secs', 'music_library_name', 'music_title')
    music_cue_id = sgqlc.types.Field(String, graphql_name='musicCueId')
    music_duration_secs = sgqlc.types.Field(Int, graphql_name='musicDurationSecs')
    music_library_name = sgqlc.types.Field(String, graphql_name='musicLibraryName')
    music_title = sgqlc.types.Field(String, graphql_name='musicTitle')


class Mutation(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('create_article', 'create_audio', 'create_audio_asset', 'create_cheerleader_person', 'create_club_injury_report', 'create_club_transaction', 'create_coach_person', 'create_content_list', 'create_current_club_depth_chart', 'create_current_club_roster', 'create_current_contextual', 'create_depth_chart_position_order', 'create_draft', 'create_draft_pick', 'create_draft_team', 'create_elias_prospect', 'create_event', 'create_executive_person', 'create_game', 'create_image', 'create_image_asset', 'create_injury_report', 'create_meta', 'create_milestone_player', 'create_milestone_team', 'create_mock_draft', 'create_mock_draft_pick', 'create_new_author', 'create_new_cheerleader', 'create_new_coach', 'create_new_executive', 'create_new_prospect', 'create_person_list', 'create_promo', 'create_season', 'create_series', 'create_show', 'create_tag', 'create_team', 'create_video', 'create_video_asset', 'create_week', 'delete_current_club_depth_chart', 'delete_current_club_roster', 'delete_draft_pick', 'delete_game', 'delete_injury_report', 'fantasy_celebration_delete', 'fantasy_celebration_save', 'game_insight_delete', 'game_insight_save', 'generate_smart_id', 'heimdallr', 'mvpd_add_identity_providers_to_group', 'mvpd_clear_identity_provider_group', 'mvpd_create_black_list', 'mvpd_create_identity_provider', 'mvpd_create_identity_provider_group', 'mvpd_delete_black_list', 'mvpd_delete_identity_provider', 'search_create_content', 'search_create_keyword', 'search_delete_content', 'search_delete_keyword', 'update_elias_prospect', 'update_franchise', 'update_game', 'update_player_person', 'update_team', 'update_video')
    create_article = sgqlc.types.Field('CreateArticlePayload', graphql_name='createArticle', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateArticleInput), graphql_name='input', default=None)),
))
    )
    create_audio = sgqlc.types.Field('CreateAudioPayload', graphql_name='createAudio', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAudioInput), graphql_name='input', default=None)),
))
    )
    create_audio_asset = sgqlc.types.Field('CreateAudioAssetPayload', graphql_name='createAudioAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAudioAssetInput), graphql_name='input', default=None)),
))
    )
    create_cheerleader_person = sgqlc.types.Field('CreateCheerleaderPersonPayload', graphql_name='createCheerleaderPerson', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCheerleaderPersonInput), graphql_name='input', default=None)),
))
    )
    create_club_injury_report = sgqlc.types.Field('CreateClubInjuryReportPayload', graphql_name='createClubInjuryReport', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateClubInjuryReportInput), graphql_name='input', default=None)),
))
    )
    create_club_transaction = sgqlc.types.Field('CreateClubTransactionPayload', graphql_name='createClubTransaction', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateClubTransactionInput), graphql_name='input', default=None)),
))
    )
    create_coach_person = sgqlc.types.Field('CreateCoachPersonPayload', graphql_name='createCoachPerson', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCoachPersonInput), graphql_name='input', default=None)),
))
    )
    create_content_list = sgqlc.types.Field('CreateContentListPayload', graphql_name='createContentList', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateContentListInput), graphql_name='input', default=None)),
))
    )
    create_current_club_depth_chart = sgqlc.types.Field('CreateCurrentClubDepthChartPayload', graphql_name='createCurrentClubDepthChart', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCurrentClubDepthChartInput), graphql_name='input', default=None)),
))
    )
    create_current_club_roster = sgqlc.types.Field('CreateCurrentClubRosterPayload', graphql_name='createCurrentClubRoster', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCurrentClubRosterInput), graphql_name='input', default=None)),
))
    )
    create_current_contextual = sgqlc.types.Field('CreateCurrentContextualPayload', graphql_name='createCurrentContextual', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCurrentContextualInput), graphql_name='input', default=None)),
))
    )
    create_depth_chart_position_order = sgqlc.types.Field('CreateDepthChartPositionOrderPayload', graphql_name='createDepthChartPositionOrder', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDepthChartPositionOrderInput), graphql_name='input', default=None)),
))
    )
    create_draft = sgqlc.types.Field('CreateDraftPayload', graphql_name='createDraft', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDraftInput), graphql_name='input', default=None)),
))
    )
    create_draft_pick = sgqlc.types.Field('CreateDraftPickPayload', graphql_name='createDraftPick', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDraftPickInput), graphql_name='input', default=None)),
))
    )
    create_draft_team = sgqlc.types.Field('CreateDraftTeamPayload', graphql_name='createDraftTeam', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateDraftTeamInput), graphql_name='input', default=None)),
))
    )
    create_elias_prospect = sgqlc.types.Field('CreateProspectPayload', graphql_name='createEliasProspect', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateEliasProspectInput), graphql_name='input', default=None)),
))
    )
    create_event = sgqlc.types.Field('CreateEventPayload', graphql_name='createEvent', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateEventInput), graphql_name='input', default=None)),
))
    )
    create_executive_person = sgqlc.types.Field('CreateExecutivePersonPayload', graphql_name='createExecutivePerson', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateExecutivePersonInput), graphql_name='input', default=None)),
))
    )
    create_game = sgqlc.types.Field('CreateGamePayload', graphql_name='createGame', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateGameInput), graphql_name='input', default=None)),
))
    )
    create_image = sgqlc.types.Field('CreateImagePayload', graphql_name='createImage', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateImageInput), graphql_name='input', default=None)),
))
    )
    create_image_asset = sgqlc.types.Field('CreateImageAssetPayload', graphql_name='createImageAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateImageAssetInput), graphql_name='input', default=None)),
))
    )
    create_injury_report = sgqlc.types.Field('CreateInjuryReportPayload', graphql_name='createInjuryReport', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateInjuryReportInput), graphql_name='input', default=None)),
))
    )
    create_meta = sgqlc.types.Field('CreateMetaPayload', graphql_name='createMeta', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMetaInput), graphql_name='input', default=None)),
))
    )
    create_milestone_player = sgqlc.types.Field('CreateMilestonePlayerPayload', graphql_name='createMilestonePlayer', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMilestonePlayerInput), graphql_name='input', default=None)),
))
    )
    create_milestone_team = sgqlc.types.Field('CreateMilestoneTeamPayload', graphql_name='createMilestoneTeam', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMilestoneTeamInput), graphql_name='input', default=None)),
))
    )
    create_mock_draft = sgqlc.types.Field('CreateMockDraftPayload', graphql_name='createMockDraft', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMockDraftInput), graphql_name='input', default=None)),
))
    )
    create_mock_draft_pick = sgqlc.types.Field('CreateMockDraftPickPayload', graphql_name='createMockDraftPick', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateMockDraftPickInput), graphql_name='input', default=None)),
))
    )
    create_new_author = sgqlc.types.Field('CreateAuthorPersonPayload', graphql_name='createNewAuthor', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAuthorPersonInput), graphql_name='input', default=None)),
))
    )
    create_new_cheerleader = sgqlc.types.Field('CreateCheerleaderPayload', graphql_name='createNewCheerleader', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCheerleaderInput), graphql_name='input', default=None)),
))
    )
    create_new_coach = sgqlc.types.Field('CreateCoachPayload', graphql_name='createNewCoach', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCoachInput), graphql_name='input', default=None)),
))
    )
    create_new_executive = sgqlc.types.Field('CreateExecutivePayload', graphql_name='createNewExecutive', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateExecutiveInput), graphql_name='input', default=None)),
))
    )
    create_new_prospect = sgqlc.types.Field('CreateProspectPayload', graphql_name='createNewProspect', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateProspectInput), graphql_name='input', default=None)),
))
    )
    create_person_list = sgqlc.types.Field('CreatePersonListPayload', graphql_name='createPersonList', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreatePersonListInput), graphql_name='input', default=None)),
))
    )
    create_promo = sgqlc.types.Field('CreatePromoPayload', graphql_name='createPromo', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreatePromoInput), graphql_name='input', default=None)),
))
    )
    create_season = sgqlc.types.Field('CreateSeasonPayload', graphql_name='createSeason', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSeasonInput), graphql_name='input', default=None)),
))
    )
    create_series = sgqlc.types.Field('CreateSeriesPayload', graphql_name='createSeries', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateSeriesInput), graphql_name='input', default=None)),
))
    )
    create_show = sgqlc.types.Field('CreateShowPayload', graphql_name='createShow', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateShowInput), graphql_name='input', default=None)),
))
    )
    create_tag = sgqlc.types.Field('CreateTagPayload', graphql_name='createTag', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateTagInput), graphql_name='input', default=None)),
))
    )
    create_team = sgqlc.types.Field('CreateTeamPayload', graphql_name='createTeam', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateTeamInput), graphql_name='input', default=None)),
))
    )
    create_video = sgqlc.types.Field('CreateVideoPayload', graphql_name='createVideo', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateVideoInput), graphql_name='input', default=None)),
))
    )
    create_video_asset = sgqlc.types.Field('CreateVideoAssetPayload', graphql_name='createVideoAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateVideoAssetInput), graphql_name='input', default=None)),
))
    )
    create_week = sgqlc.types.Field('CreateWeekPayload', graphql_name='createWeek', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SaveWeekInput), graphql_name='input', default=None)),
))
    )
    delete_current_club_depth_chart = sgqlc.types.Field('CommonVoidPayload', graphql_name='deleteCurrentClubDepthChart', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCurrentClubDepthChartInput), graphql_name='input', default=None)),
))
    )
    delete_current_club_roster = sgqlc.types.Field('CommonVoidPayload', graphql_name='deleteCurrentClubRoster', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCurrentClubRosterInput), graphql_name='input', default=None)),
))
    )
    delete_draft_pick = sgqlc.types.Field('CommonVoidPayload', graphql_name='deleteDraftPick', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteDraftPickInput), graphql_name='input', default=None)),
))
    )
    delete_game = sgqlc.types.Field('CommonVoidPayload', graphql_name='deleteGame', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CommonIdInput), graphql_name='input', default=None)),
))
    )
    delete_injury_report = sgqlc.types.Field('CommonVoidPayload', graphql_name='deleteInjuryReport', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteInjuryReportInput), graphql_name='input', default=None)),
))
    )
    fantasy_celebration_delete = sgqlc.types.Field('CommonVoidPayload', graphql_name='fantasyCelebrationDelete', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCelebrationInput), graphql_name='input', default=None)),
))
    )
    fantasy_celebration_save = sgqlc.types.Field('CelebrationPayload', graphql_name='fantasyCelebrationSave', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SaveCelebrationInput), graphql_name='input', default=None)),
))
    )
    game_insight_delete = sgqlc.types.Field('CommonVoidPayload', graphql_name='gameInsightDelete', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteGameInsightInput), graphql_name='input', default=None)),
))
    )
    game_insight_save = sgqlc.types.Field('GameInsightPayload', graphql_name='gameInsightSave', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SaveGameInsightInput), graphql_name='input', default=None)),
))
    )
    generate_smart_id = sgqlc.types.Field('GenerateSmartIDPayload', graphql_name='generateSmartID', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(GenerateSmartIDInput), graphql_name='input', default=None)),
))
    )
    heimdallr = sgqlc.types.Field('HeimdallrPayload', graphql_name='heimdallr', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(HeimdallrInput), graphql_name='input', default=None)),
))
    )
    mvpd_add_identity_providers_to_group = sgqlc.types.Field('CommonIdentityProviderGroupPayload', graphql_name='mvpdAddIdentityProvidersToGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(AddIdentityProvidersToGroupInput), graphql_name='input', default=None)),
))
    )
    mvpd_clear_identity_provider_group = sgqlc.types.Field('ClearIdentityProviderGroupPayload', graphql_name='mvpdClearIdentityProviderGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ClearIdentityProviderGroupInput), graphql_name='input', default=None)),
))
    )
    mvpd_create_black_list = sgqlc.types.Field('BlackListPayload', graphql_name='mvpdCreateBlackList', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateBlackListInput), graphql_name='input', default=None)),
))
    )
    mvpd_create_identity_provider = sgqlc.types.Field('CommonIdentityProviderPayload', graphql_name='mvpdCreateIdentityProvider', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateIdentityProviderInput), graphql_name='input', default=None)),
))
    )
    mvpd_create_identity_provider_group = sgqlc.types.Field('CommonIdentityProviderGroupPayload', graphql_name='mvpdCreateIdentityProviderGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateIdentityProviderGroupInput), graphql_name='input', default=None)),
))
    )
    mvpd_delete_black_list = sgqlc.types.Field('CommonVoidPayload', graphql_name='mvpdDeleteBlackList', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteBlackListInput), graphql_name='input', default=None)),
))
    )
    mvpd_delete_identity_provider = sgqlc.types.Field('CommonVoidPayload', graphql_name='mvpdDeleteIdentityProvider', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteIdentityProviderInput), graphql_name='input', default=None)),
))
    )
    search_create_content = sgqlc.types.Field('ShieldSearchContentPayload', graphql_name='searchCreateContent', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateContentInput), graphql_name='input', default=None)),
))
    )
    search_create_keyword = sgqlc.types.Field('ShieldSearchKeyValuePayload', graphql_name='searchCreateKeyword', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateKeywordInput), graphql_name='input', default=None)),
))
    )
    search_delete_content = sgqlc.types.Field('ShieldSearchContentPayload', graphql_name='searchDeleteContent', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(RemoveContentInput), graphql_name='input', default=None)),
))
    )
    search_delete_keyword = sgqlc.types.Field('ShieldSearchKeyValuePayload', graphql_name='searchDeleteKeyword', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(RemoveKeywordInput), graphql_name='input', default=None)),
))
    )
    update_elias_prospect = sgqlc.types.Field('CreateProspectPayload', graphql_name='updateEliasProspect', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateEliasProspectInput), graphql_name='input', default=None)),
))
    )
    update_franchise = sgqlc.types.Field('UpdateFranchisePayload', graphql_name='updateFranchise', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateFranchiseInput), graphql_name='input', default=None)),
))
    )
    update_game = sgqlc.types.Field('UpdateGamePayload', graphql_name='updateGame', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateGameInput), graphql_name='input', default=None)),
))
    )
    update_player_person = sgqlc.types.Field('UpdatePlayerPersonPayload', graphql_name='updatePlayerPerson', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdatePlayerPersonInput), graphql_name='input', default=None)),
))
    )
    update_team = sgqlc.types.Field('UpdateTeamPayload', graphql_name='updateTeam', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateTeamInput), graphql_name='input', default=None)),
))
    )
    update_video = sgqlc.types.Field('CreateVideoPayload', graphql_name='updateVideo', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateVideoInput), graphql_name='input', default=None)),
))
    )


class MvpdGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('mvpd_black_list', 'mvpd_black_lists', 'mvpd_black_lists_country_and_dma', 'mvpd_identity_provider', 'mvpd_identity_provider_group', 'mvpd_identity_provider_groups', 'mvpd_identity_providers')
    mvpd_black_list = sgqlc.types.Field(BlackList, graphql_name='mvpdBlackList', args=sgqlc.types.ArgDict((
        ('country_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='countryCode', default=None)),
        ('dma_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dmaCode', default=None)),
        ('network', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='network', default=None)),
        ('identity_provider_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='identityProviderId', default=None)),
))
    )
    mvpd_black_lists = sgqlc.types.Field(sgqlc.types.list_of(BlackList), graphql_name='mvpdBlackLists')
    mvpd_black_lists_country_and_dma = sgqlc.types.Field(sgqlc.types.list_of(BlackList), graphql_name='mvpdBlackListsCountryAndDma', args=sgqlc.types.ArgDict((
        ('country_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='countryCode', default=None)),
        ('dma_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dmaCode', default=None)),
))
    )
    mvpd_identity_provider = sgqlc.types.Field('IdentityProvider', graphql_name='mvpdIdentityProvider', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    mvpd_identity_provider_group = sgqlc.types.Field('IdentityProviderGroup', graphql_name='mvpdIdentityProviderGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    mvpd_identity_provider_groups = sgqlc.types.Field(sgqlc.types.list_of('IdentityProviderGroup'), graphql_name='mvpdIdentityProviderGroups', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.list_of(ID), graphql_name='ids', default=None)),
        ('names', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='names', default=None)),
        ('identity_provider_id', sgqlc.types.Arg(String, graphql_name='identityProviderId', default=None)),
))
    )
    mvpd_identity_providers = sgqlc.types.Field(sgqlc.types.list_of('IdentityProvider'), graphql_name='mvpdIdentityProviders', args=sgqlc.types.ArgDict((
        ('filter_type', sgqlc.types.Arg(IdpFilterType, graphql_name='filterType', default=None)),
))
    )


class NetworkGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('show', 'shows', 'shows_by_ids')
    show = sgqlc.types.Field('Show', graphql_name='show', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    shows = sgqlc.types.Field('ShowConnection', graphql_name='shows', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(NameOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
))
    )
    shows_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Show'), graphql_name='showsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class Node(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class PageInfoWithTotal(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('has_next_page', 'has_previous_page', 'start_cursor', 'end_cursor', 'previous_page_start_cursor', 'total')
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasPreviousPage')
    start_cursor = sgqlc.types.Field(String, graphql_name='startCursor')
    end_cursor = sgqlc.types.Field(String, graphql_name='endCursor')
    previous_page_start_cursor = sgqlc.types.Field(String, graphql_name='previousPageStartCursor')
    total = sgqlc.types.Field(BigInteger, graphql_name='total')


class PersonListConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PersonListEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PersonListEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('PersonList'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PersonsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('author', 'authors', 'authors_by_ids', 'cheerleader', 'cheerleader_person', 'cheerleader_persons', 'cheerleader_persons_by_ids', 'cheerleaders', 'cheerleaders_by_ids', 'coach', 'coach_person', 'coach_persons', 'coach_persons_by_ids', 'coaches', 'coaches_by_ids', 'executive', 'executive_person', 'executive_persons', 'executive_persons_by_ids', 'executives', 'executives_by_ids', 'metadata', 'person', 'persons', 'persons_by_ids', 'player', 'player_awards', 'player_by_gsis_shield_id', 'players', 'players_by_ids', 'prospect', 'prospect_by_person', 'prospects', 'prospects_by_ids')
    author = sgqlc.types.Field('AuthorPerson', graphql_name='author', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    authors = sgqlc.types.Field(AuthorPersonConnection, graphql_name='authors', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(AuthorOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
))
    )
    authors_by_ids = sgqlc.types.Field(sgqlc.types.list_of('AuthorPerson'), graphql_name='authorsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    cheerleader = sgqlc.types.Field('Cheerleader', graphql_name='cheerleader', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    cheerleader_person = sgqlc.types.Field('CheerleaderPerson', graphql_name='cheerleaderPerson', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    cheerleader_persons = sgqlc.types.Field(CheerleaderPersonConnection, graphql_name='cheerleaderPersons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PersonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('status', sgqlc.types.Arg(Status, graphql_name='status', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    cheerleader_persons_by_ids = sgqlc.types.Field(sgqlc.types.list_of('CheerleaderPerson'), graphql_name='cheerleaderPersonsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    cheerleaders = sgqlc.types.Field(CheerleaderConnection, graphql_name='cheerleaders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(CheerleaderOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('cheerleader_person_display_name', sgqlc.types.Arg(String, graphql_name='cheerleaderPerson_displayName', default=None)),
        ('cheerleader_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='cheerleaderPerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    cheerleaders_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Cheerleader'), graphql_name='cheerleadersByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    coach = sgqlc.types.Field('Coach', graphql_name='coach', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    coach_person = sgqlc.types.Field('CoachPerson', graphql_name='coachPerson', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    coach_persons = sgqlc.types.Field(CoachPersonConnection, graphql_name='coachPersons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PersonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('status', sgqlc.types.Arg(Status, graphql_name='status', default=None)),
        ('coach_type', sgqlc.types.Arg(CoachType, graphql_name='coachType', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    coach_persons_by_ids = sgqlc.types.Field(sgqlc.types.list_of('CoachPerson'), graphql_name='coachPersonsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    coaches = sgqlc.types.Field(CoachConnection, graphql_name='coaches', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(CoachOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('coach_person_display_name', sgqlc.types.Arg(String, graphql_name='coachPerson_displayName', default=None)),
        ('coach_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='coachPerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    coaches_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Coach'), graphql_name='coachesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    executive = sgqlc.types.Field('Executive', graphql_name='executive', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    executive_person = sgqlc.types.Field('ExecutivePerson', graphql_name='executivePerson', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    executive_persons = sgqlc.types.Field(ExecutivePersonConnection, graphql_name='executivePersons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PersonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('status', sgqlc.types.Arg(Status, graphql_name='status', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    executive_persons_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ExecutivePerson'), graphql_name='executivePersonsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    executives = sgqlc.types.Field(ExecutiveConnection, graphql_name='executives', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ExecutiveOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('executive_person_display_name', sgqlc.types.Arg(String, graphql_name='executivePerson_displayName', default=None)),
        ('executive_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='executivePerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(WorkStatus, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    executives_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Executive'), graphql_name='executivesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    metadata = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Meta)), graphql_name='metadata', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('entity_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='entityType', default=None)),
        ('entity_id', sgqlc.types.Arg(String, graphql_name='entityId', default=None)),
))
    )
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    persons = sgqlc.types.Field('PlayerPersonConnection', graphql_name='persons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PersonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('last_name_beginswith', sgqlc.types.Arg(String, graphql_name='lastNameBEGINSWITH', default=None)),
        ('current_profile', sgqlc.types.Arg(ProfileType, graphql_name='currentProfile', default=None)),
        ('status', sgqlc.types.Arg(Status, graphql_name='status', default=None)),
))
    )
    persons_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerPerson'), graphql_name='personsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    player = sgqlc.types.Field('Player', graphql_name='player', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_awards = sgqlc.types.Field('PlayerAwardConnection', graphql_name='playerAwards', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PlayerAwardsOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_id', sgqlc.types.Arg(String, graphql_name='personId', default=None)),
        ('season_value', sgqlc.types.Arg(Int, graphql_name='seasonValue', default=None)),
        ('award_type', sgqlc.types.Arg(String, graphql_name='awardType', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
))
    )
    player_by_gsis_shield_id = sgqlc.types.Field('Player', graphql_name='playerByGsisShieldId', args=sgqlc.types.ArgDict((
        ('gsis_shield_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='gsisShieldId', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
))
    )
    players = sgqlc.types.Field('PlayerConnection', graphql_name='players', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PlayerOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('person_last_name_beginswith', sgqlc.types.Arg(String, graphql_name='person_lastNameBEGINSWITH', default=None)),
        ('status', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='status', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    players_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Player'), graphql_name='playersByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    prospect = sgqlc.types.Field('Prospect', graphql_name='prospect', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    prospect_by_person = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Prospect')), graphql_name='prospectByPerson', args=sgqlc.types.ArgDict((
        ('person_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='person_id', default=None)),
))
    )
    prospects = sgqlc.types.Field('ProspectConnection', graphql_name='prospects', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ProspectOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='year', default=None)),
))
    )
    prospects_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Prospect'), graphql_name='prospectsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class PlayerAwardConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerAwardEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerAwardEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('PlayerAward'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Player'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerGameStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerGameStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerGameStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avg_yds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_tackles_for_aloss', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_first_downs', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'passing_40plus_yards_each', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'start_position', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avg_yds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgYds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_tackles_for_aloss = sgqlc.types.Field(Float, graphql_name='defensiveTacklesForALoss')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    passing_40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing_40plusYardsEach')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    start_position = sgqlc.types.Field(String, graphql_name='startPosition')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class PlayerGameStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('PlayerGameStats'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerPersonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerPersonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerPersonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('PlayerPerson'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerSeasonSplitStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_first_downs', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'split_category', 'split_subcategory', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    split_category = sgqlc.types.Field(String, graphql_name='splitCategory')
    split_subcategory = sgqlc.types.Field(String, graphql_name='splitSubcategory')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class PlayerSeasonStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_firstdowns', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_firstdowns = sgqlc.types.Field(Int, graphql_name='passingFirstdowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class PlayerStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('PlayerStats'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerStatsLeaders(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'defensive_assists', 'defensive_interceptions', 'defensive_sacks', 'defensive_total_tackles', 'firstdowns_total', 'kick_returns', 'kicking_fg_made', 'passing_net_yards', 'passing_yards', 'player', 'punting_yards', 'receiving_yards', 'rushing_yards', 'total_points_scored', 'total_tackles', 'touchdowns_total')
    current_team_id = sgqlc.types.Field(String, graphql_name='currentTeamId')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    player = sgqlc.types.Field('Player', graphql_name='player')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    total_tackles = sgqlc.types.Field(Float, graphql_name='totalTackles')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class PlayerStatsLeadersConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PlayerStatsLeadersEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PlayerStatsLeadersEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(PlayerStatsLeaders, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PlayerTeam(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('elias_team_id', 'esb_id', 'player_team_id', 'season_value', 'status', 'team_seq')
    elias_team_id = sgqlc.types.Field(String, graphql_name='eliasTeamId')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    player_team_id = sgqlc.types.Field(String, graphql_name='playerTeamId')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    status = sgqlc.types.Field(String, graphql_name='status')
    team_seq = sgqlc.types.Field(Int, graphql_name='teamSeq')


class PlayerTeamStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_firstdowns', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'team_id', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_firstdowns = sgqlc.types.Field(Int, graphql_name='passingFirstdowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class PlayerTotalCareerStats(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('person', 'season_stats', 'season_type')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    season_stats = sgqlc.types.Field(PlayerSeasonStatsDetail, graphql_name='seasonStats')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')


class PromoConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PromoEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PromoEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Promo'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PropertyConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('PropertyEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class PropertyEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Property'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ProspectConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ProspectEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class ProspectEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Prospect'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class PublishedContentGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('published_article', 'published_articles', 'published_articles_by_ids', 'published_audio', 'published_audios', 'published_audios_by_ids', 'published_content_list', 'published_content_list_by_tag', 'published_content_lists', 'published_content_lists_by_ids', 'published_event', 'published_events', 'published_events_by_ids', 'published_image', 'published_images', 'published_images_by_ids', 'published_person_list', 'published_person_list_by_tag', 'published_person_lists', 'published_person_lists_by_ids', 'published_promo', 'published_promos', 'published_promos_by_ids', 'published_video', 'published_videos', 'published_videos_by_ids')
    published_article = sgqlc.types.Field('Article', graphql_name='publishedArticle', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_articles = sgqlc.types.Field(ArticleConnection, graphql_name='publishedArticles', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    published_articles_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Article'), graphql_name='publishedArticlesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_audio = sgqlc.types.Field('Audio', graphql_name='publishedAudio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_audios = sgqlc.types.Field(AudioConnection, graphql_name='publishedAudios', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    published_audios_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Audio'), graphql_name='publishedAudiosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_content_list = sgqlc.types.Field('ContentList', graphql_name='publishedContentList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_content_list_by_tag = sgqlc.types.Field('ContentList', graphql_name='publishedContentListByTag', args=sgqlc.types.ArgDict((
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    published_content_lists = sgqlc.types.Field(ContentListConnection, graphql_name='publishedContentLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('content_hints', sgqlc.types.Arg(ContentHint, graphql_name='contentHints', default=None)),
        ('external_id', sgqlc.types.Arg(String, graphql_name='externalId', default=None)),
))
    )
    published_content_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ContentList'), graphql_name='publishedContentListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_event = sgqlc.types.Field('Event', graphql_name='publishedEvent', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_events = sgqlc.types.Field(EventConnection, graphql_name='publishedEvents', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(NameOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
))
    )
    published_events_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Event'), graphql_name='publishedEventsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_image = sgqlc.types.Field('Image', graphql_name='publishedImage', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_images = sgqlc.types.Field(ImageConnection, graphql_name='publishedImages', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    published_images_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Image'), graphql_name='publishedImagesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_person_list = sgqlc.types.Field('PersonList', graphql_name='publishedPersonList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_person_list_by_tag = sgqlc.types.Field('PersonList', graphql_name='publishedPersonListByTag', args=sgqlc.types.ArgDict((
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    published_person_lists = sgqlc.types.Field(PersonListConnection, graphql_name='publishedPersonLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
))
    )
    published_person_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PersonList'), graphql_name='publishedPersonListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_promo = sgqlc.types.Field('Promo', graphql_name='publishedPromo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_promos = sgqlc.types.Field(PromoConnection, graphql_name='publishedPromos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
))
    )
    published_promos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Promo'), graphql_name='publishedPromosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_video = sgqlc.types.Field('Video', graphql_name='publishedVideo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    published_videos = sgqlc.types.Field('VideoConnection', graphql_name='publishedVideos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('last_modified_date_daterange', sgqlc.types.Arg(String, graphql_name='lastModifiedDateDATERANGE', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('video_asset_id_exists', sgqlc.types.Arg(Existence, graphql_name='videoAsset_idEXISTS', default=None)),
))
    )
    published_videos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Video'), graphql_name='publishedVideosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )


class RegionalGame(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('blacklist', 'call_signs', 'country_abbr', 'event_radius_info', 'lat_long', 'redzone_available', 'redzone_roles', 'whitelist', 'zip_code')
    blacklist = sgqlc.types.Field(sgqlc.types.list_of(BroadcastGame), graphql_name='blacklist')
    call_signs = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='callSigns')
    country_abbr = sgqlc.types.Field(String, graphql_name='countryAbbr')
    event_radius_info = sgqlc.types.Field(EventRadiusInfo, graphql_name='eventRadiusInfo')
    lat_long = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='latLong')
    redzone_available = sgqlc.types.Field(Boolean, graphql_name='redzoneAvailable')
    redzone_roles = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='redzoneRoles')
    whitelist = sgqlc.types.Field(sgqlc.types.list_of(BroadcastGame), graphql_name='whitelist')
    zip_code = sgqlc.types.Field(String, graphql_name='zipCode')


class RelayMutationType(sgqlc.types.Interface):
    __schema__ = shield
    __field_names__ = ('client_mutation_id',)
    client_mutation_id = sgqlc.types.Field(String, graphql_name='clientMutationId')


class Root(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('article', 'articles', 'articles_by_ids', 'assets', 'audio', 'audio_asset', 'audio_assets', 'audio_assets_by_ids', 'audios', 'audios_by_ids', 'author', 'authors', 'authors_by_ids', 'cheerleader', 'cheerleaders', 'cheerleaders_by_ids', 'club_transaction', 'club_transactions', 'club_transactions_by_ids', 'clubs', 'coach', 'coaches', 'coaches_by_ids', 'content', 'content_list', 'content_list_by_tag', 'content_lists', 'content_lists_by_ids', 'current_season', 'current_season_type', 'current_week', 'decode_smart_id', 'draft', 'drafts', 'drafts_by_ids', 'elias', 'elias_stats_group', 'event', 'events', 'events_by_ids', 'executive', 'executives', 'executives_by_ids', 'fantasy_celebration', 'favorite_teams_by_country_and_postal_code', 'franchise', 'franchises', 'franchises_by_ids', 'game', 'game_detail', 'game_details_by_ids', 'game_insight', 'games', 'games_by_ids', 'heimdallr_info', 'image', 'image_asset', 'image_assets', 'image_assets_by_ids', 'images', 'images_by_ids', 'injury_report', 'injury_reports', 'injury_reports_by_ids', 'keycount', 'league', 'live', 'media', 'media_token', 'media_with_token', 'mvpd', 'network', 'node', 'nodes', 'person', 'person_list', 'person_list_by_tag', 'person_lists', 'person_lists_by_ids', 'persons', 'persons_by_ids', 'persons_group', 'player', 'player_game_stat', 'player_game_stats', 'player_game_stats_by_ids', 'player_stat', 'player_stats', 'player_stats_by_ids', 'players', 'players_by_ids', 'promo', 'promos', 'promos_by_ids', 'properties', 'properties_by_ids', 'property', 'property_id_to_franchise_id_map', 'prospect', 'prospects', 'prospects_by_ids', 'published_content', 'regional_game_by_country', 'regional_game_by_dma', 'regional_game_by_lat_long', 'regional_game_by_zip', 'search', 'search_autocomplete', 'search_closest_word', 'search_feeling_lucky', 'search_group', 'search_keywords', 'season', 'seasons', 'show', 'shows', 'shows_by_ids', 'standing', 'standings', 'standings_by_ids', 'stats', 'tag', 'tags', 'tags_by_ids', 'team', 'team_game_stat', 'team_game_stats', 'team_game_stats_by_ids', 'team_stat', 'team_stats', 'team_stats_by_ids', 'teams', 'teams_by_ids', 'teams_group', 'video', 'video_asset', 'video_assets', 'video_assets_by_ids', 'videos', 'videos_by_ids', 'zeppelin_info')
    article = sgqlc.types.Field('Article', graphql_name='article', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    articles = sgqlc.types.Field(ArticleConnection, graphql_name='articles', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    articles_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Article'), graphql_name='articlesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    assets = sgqlc.types.Field(AssetsGroup, graphql_name='assets')
    audio = sgqlc.types.Field('Audio', graphql_name='audio', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    audio_asset = sgqlc.types.Field('AudioAsset', graphql_name='audioAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    audio_assets = sgqlc.types.Field(AudioAssetConnection, graphql_name='audioAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    audio_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('AudioAsset'), graphql_name='audioAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    audios = sgqlc.types.Field(AudioConnection, graphql_name='audios', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    audios_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Audio'), graphql_name='audiosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    author = sgqlc.types.Field('AuthorPerson', graphql_name='author', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    authors = sgqlc.types.Field(AuthorPersonConnection, graphql_name='authors', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(AuthorOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
))
    )
    authors_by_ids = sgqlc.types.Field(sgqlc.types.list_of('AuthorPerson'), graphql_name='authorsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    cheerleader = sgqlc.types.Field('Cheerleader', graphql_name='cheerleader', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    cheerleaders = sgqlc.types.Field(CheerleaderConnection, graphql_name='cheerleaders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(CheerleaderOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('cheerleader_person_display_name', sgqlc.types.Arg(String, graphql_name='cheerleaderPerson_displayName', default=None)),
        ('cheerleader_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='cheerleaderPerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(String, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    cheerleaders_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Cheerleader'), graphql_name='cheerleadersByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    club_transaction = sgqlc.types.Field('ClubTransaction', graphql_name='clubTransaction', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    club_transactions = sgqlc.types.Field(ClubTransactionConnection, graphql_name='clubTransactions', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(TransactionOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
        ('publish_state', sgqlc.types.Arg(PublishState, graphql_name='publishState', default=None)),
        ('transaction_year', sgqlc.types.Arg(Int, graphql_name='transactionYear', default=None)),
        ('franchise_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise_id', default=None)),
))
    )
    club_transactions_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ClubTransaction'), graphql_name='clubTransactionsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    clubs = sgqlc.types.Field(ClubsGroup, graphql_name='clubs')
    coach = sgqlc.types.Field('Coach', graphql_name='coach', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    coaches = sgqlc.types.Field(CoachConnection, graphql_name='coaches', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(CoachOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('coach_person_display_name', sgqlc.types.Arg(String, graphql_name='coachPerson_displayName', default=None)),
        ('coach_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='coachPerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(String, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    coaches_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Coach'), graphql_name='coachesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    content = sgqlc.types.Field(ContentGroup, graphql_name='content')
    content_list = sgqlc.types.Field('ContentList', graphql_name='contentList', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    content_list_by_tag = sgqlc.types.Field('ContentList', graphql_name='contentListByTag', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    content_lists = sgqlc.types.Field(ContentListConnection, graphql_name='contentLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('content_hints', sgqlc.types.Arg(ContentHint, graphql_name='contentHints', default=None)),
        ('external_id', sgqlc.types.Arg(String, graphql_name='externalId', default=None)),
))
    )
    content_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ContentList'), graphql_name='contentListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    current_season = sgqlc.types.Field(Map, graphql_name='currentSeason')
    current_season_type = sgqlc.types.Field(Map, graphql_name='currentSeasonType')
    current_week = sgqlc.types.Field(Map, graphql_name='currentWeek')
    decode_smart_id = sgqlc.types.Field(sgqlc.types.list_of(LegacyIdInfo), graphql_name='decodeSmartID', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    draft = sgqlc.types.Field('Draft', graphql_name='draft', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    drafts = sgqlc.types.Field(DraftConnection, graphql_name='drafts', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(YearOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('year', sgqlc.types.Arg(Int, graphql_name='year', default=None)),
))
    )
    drafts_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Draft'), graphql_name='draftsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    elias = sgqlc.types.Field(EliasGroup, graphql_name='elias')
    elias_stats_group = sgqlc.types.Field(EliasStatsGroup, graphql_name='eliasStatsGroup')
    event = sgqlc.types.Field('Event', graphql_name='event', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    events = sgqlc.types.Field(EventConnection, graphql_name='events', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(NameOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
))
    )
    events_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Event'), graphql_name='eventsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    executive = sgqlc.types.Field('Executive', graphql_name='executive', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    executives = sgqlc.types.Field(ExecutiveConnection, graphql_name='executives', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ExecutiveOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('executive_person_display_name', sgqlc.types.Arg(String, graphql_name='executivePerson_displayName', default=None)),
        ('executive_person_display_name_contains', sgqlc.types.Arg(String, graphql_name='executivePerson_displayNameCONTAINS', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('work_status', sgqlc.types.Arg(String, graphql_name='workStatus', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    executives_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Executive'), graphql_name='executivesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    fantasy_celebration = sgqlc.types.Field(FantasyCelebrationGroup, graphql_name='fantasyCelebration')
    favorite_teams_by_country_and_postal_code = sgqlc.types.Field(FavoriteTeams, graphql_name='favoriteTeamsByCountryAndPostalCode', args=sgqlc.types.ArgDict((
        ('country_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='countryCode', default=None)),
        ('postal_code', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='postalCode', default=None)),
))
    )
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    franchises = sgqlc.types.Field(FranchiseConnection, graphql_name='franchises', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(FranchiseOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('state', sgqlc.types.Arg(FranchiseState, graphql_name='state', default=None)),
))
    )
    franchises_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Franchise'), graphql_name='franchisesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    game = sgqlc.types.Field('Game', graphql_name='game', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    game_detail = sgqlc.types.Field('GameDetail', graphql_name='gameDetail', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    game_details_by_ids = sgqlc.types.Field(sgqlc.types.list_of('GameDetail'), graphql_name='gameDetailsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    game_insight = sgqlc.types.Field(GameInsightGroup, graphql_name='gameInsight')
    games = sgqlc.types.Field(GameConnection, graphql_name='games', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('gsis_id', sgqlc.types.Arg(Int, graphql_name='gsisId', default=None)),
        ('esb_id', sgqlc.types.Arg(Int, graphql_name='esbId', default=None)),
        ('franchise_id', sgqlc.types.Arg(String, graphql_name='franchiseId', default=None)),
))
    )
    games_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Game'), graphql_name='gamesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    heimdallr_info = sgqlc.types.Field(String, graphql_name='heimdallrInfo')
    image = sgqlc.types.Field('Image', graphql_name='image', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    image_asset = sgqlc.types.Field('ImageAsset', graphql_name='imageAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    image_assets = sgqlc.types.Field(ImageAssetConnection, graphql_name='imageAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    image_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('ImageAsset'), graphql_name='imageAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    images = sgqlc.types.Field(ImageConnection, graphql_name='images', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('persons_id', sgqlc.types.Arg(String, graphql_name='persons_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    images_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Image'), graphql_name='imagesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    injury_report = sgqlc.types.Field('Injury', graphql_name='injuryReport', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    injury_reports = sgqlc.types.Field(InjuryConnection, graphql_name='injuryReports', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(InjuryReportOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
        ('team_abbreviation', sgqlc.types.Arg(String, graphql_name='team_abbreviation', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
))
    )
    injury_reports_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Injury'), graphql_name='injuryReportsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    keycount = sgqlc.types.Field(KeycountResponse, graphql_name='keycount', args=sgqlc.types.ArgDict((
        ('namespace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='namespace', default=None)),
        ('from_', sgqlc.types.Arg(sgqlc.types.non_null(DateTime), graphql_name='from', default=None)),
        ('to', sgqlc.types.Arg(sgqlc.types.non_null(DateTime), graphql_name='to', default=None)),
        ('populate_time_series', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='populateTimeSeries', default=None)),
        ('granularity', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='granularity', default=None)),
))
    )
    league = sgqlc.types.Field(LeagueGroup, graphql_name='league')
    live = sgqlc.types.Field(LiveGroup, graphql_name='live')
    media = sgqlc.types.Field(Media, graphql_name='media', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    media_token = sgqlc.types.Field('MediaToken', graphql_name='mediaToken', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('anvack', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='anvack', default=None)),
))
    )
    media_with_token = sgqlc.types.Field(Media, graphql_name='mediaWithToken', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('token', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='token', default=None)),
))
    )
    mvpd = sgqlc.types.Field(MvpdGroup, graphql_name='mvpd')
    network = sgqlc.types.Field(NetworkGroup, graphql_name='network')
    node = sgqlc.types.Field(Node, graphql_name='node', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
))
    )
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Node), graphql_name='nodes', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
))
    )
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    person_list = sgqlc.types.Field('PersonList', graphql_name='personList', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    person_list_by_tag = sgqlc.types.Field('PersonList', graphql_name='personListByTag', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('tag', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tag', default=None)),
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='property_id', default=None)),
))
    )
    person_lists = sgqlc.types.Field(PersonListConnection, graphql_name='personLists', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
))
    )
    person_lists_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PersonList'), graphql_name='personListsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    persons = sgqlc.types.Field(PlayerPersonConnection, graphql_name='persons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PersonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('display_name', sgqlc.types.Arg(String, graphql_name='displayName', default=None)),
        ('display_name_contains', sgqlc.types.Arg(String, graphql_name='displayNameCONTAINS', default=None)),
        ('current_profile', sgqlc.types.Arg(ProfileType, graphql_name='currentProfile', default=None)),
        ('status', sgqlc.types.Arg(Status, graphql_name='status', default=None)),
))
    )
    persons_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerPerson'), graphql_name='personsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    persons_group = sgqlc.types.Field(PersonsGroup, graphql_name='personsGroup')
    player = sgqlc.types.Field('Player', graphql_name='player', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_game_stat = sgqlc.types.Field('PlayerGameStats', graphql_name='playerGameStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_game_stats = sgqlc.types.Field(PlayerGameStatsConnection, graphql_name='playerGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(Int, graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='player_id', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='game_id', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    player_game_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerGameStats'), graphql_name='playerGameStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    player_stat = sgqlc.types.Field('PlayerStats', graphql_name='playerStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_stats = sgqlc.types.Field(PlayerStatsConnection, graphql_name='playerStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonTypeOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_season', sgqlc.types.Arg(Int, graphql_name='season_season', default=None)),
        ('season_type', sgqlc.types.Arg(SeasonType, graphql_name='seasonType', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='player_id', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    player_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerStats'), graphql_name='playerStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    players = sgqlc.types.Field(PlayerConnection, graphql_name='players', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PlayerOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('status', sgqlc.types.Arg(String, graphql_name='status', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeam_id', default=None)),
))
    )
    players_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Player'), graphql_name='playersByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    promo = sgqlc.types.Field('Promo', graphql_name='promo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    promos = sgqlc.types.Field(PromoConnection, graphql_name='promos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    promos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Promo'), graphql_name='promosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    properties = sgqlc.types.Field(PropertyConnection, graphql_name='properties', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(PropertyOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_type', sgqlc.types.Arg(PropertyType, graphql_name='propertyType', default=None)),
        ('enabled', sgqlc.types.Arg(Boolean, graphql_name='enabled', default=None)),
))
    )
    properties_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Property'), graphql_name='propertiesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    property = sgqlc.types.Field('Property', graphql_name='property', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    property_id_to_franchise_id_map = sgqlc.types.Field(sgqlc.types.list_of(FranchiseToPropertyPayload), graphql_name='propertyIdToFranchiseIdMap', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    prospect = sgqlc.types.Field('Prospect', graphql_name='prospect', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    prospects = sgqlc.types.Field(ProspectConnection, graphql_name='prospects', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(ProspectOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('person_display_name', sgqlc.types.Arg(String, graphql_name='person_displayName', default=None)),
        ('person_display_name_contains', sgqlc.types.Arg(String, graphql_name='person_displayNameCONTAINS', default=None)),
        ('year', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='year', default=None)),
))
    )
    prospects_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Prospect'), graphql_name='prospectsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    published_content = sgqlc.types.Field(PublishedContentGroup, graphql_name='publishedContent')
    regional_game_by_country = sgqlc.types.Field(RegionalGame, graphql_name='regionalGameByCountry', args=sgqlc.types.ArgDict((
        ('country', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='country', default=None)),
))
    )
    regional_game_by_dma = sgqlc.types.Field(RegionalGame, graphql_name='regionalGameByDma', args=sgqlc.types.ArgDict((
        ('dma', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dma', default=None)),
))
    )
    regional_game_by_lat_long = sgqlc.types.Field(RegionalGame, graphql_name='regionalGameByLatLong', args=sgqlc.types.ArgDict((
        ('lat_long', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='latLong', default=None)),
))
    )
    regional_game_by_zip = sgqlc.types.Field(RegionalGame, graphql_name='regionalGameByZip', args=sgqlc.types.ArgDict((
        ('country', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='country', default=None)),
        ('zip', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='zip', default=None)),
))
    )
    search = sgqlc.types.Field('ShieldSearch', graphql_name='search', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
        ('content_type', sgqlc.types.Arg(sgqlc.types.list_of(ContentType), graphql_name='contentType', default=None)),
        ('order_by', sgqlc.types.Arg(SearchOrderBy, graphql_name='orderBy', default=None)),
))
    )
    search_autocomplete = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='searchAutocomplete', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
))
    )
    search_closest_word = sgqlc.types.Field(String, graphql_name='searchClosestWord', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
))
    )
    search_feeling_lucky = sgqlc.types.Field('ShieldSearch', graphql_name='searchFeelingLucky', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
))
    )
    search_group = sgqlc.types.Field('SearchGroup', graphql_name='searchGroup')
    search_keywords = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='searchKeywords', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
))
    )
    season = sgqlc.types.Field('Season', graphql_name='season', args=sgqlc.types.ArgDict((
        ('season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season', default=None)),
))
    )
    seasons = sgqlc.types.Field('SeasonConnection', graphql_name='seasons', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
))
    )
    show = sgqlc.types.Field('Show', graphql_name='show', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    shows = sgqlc.types.Field('ShowConnection', graphql_name='shows', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(NameOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('workflow_status', sgqlc.types.Arg(WorkflowStatus, graphql_name='workflowStatus', default=None)),
))
    )
    shows_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Show'), graphql_name='showsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    standing = sgqlc.types.Field('Standings', graphql_name='standing', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    standings = sgqlc.types.Field('StandingsConnection', graphql_name='standings', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
))
    )
    standings_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Standings'), graphql_name='standingsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    stats = sgqlc.types.Field('StatsGroup', graphql_name='stats')
    tag = sgqlc.types.Field('Tag', graphql_name='tag', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tags')
    tags_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Tag'), graphql_name='tagsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    team = sgqlc.types.Field('Team', graphql_name='team', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    team_game_stat = sgqlc.types.Field('TeamGameStats', graphql_name='teamGameStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    team_game_stats = sgqlc.types.Field('TeamGameStatsConnection', graphql_name='teamGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(Int, graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='game_id', default=None)),
))
    )
    team_game_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('TeamGameStats'), graphql_name='teamGameStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    team_stat = sgqlc.types.Field('TeamStats', graphql_name='teamStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    team_stats = sgqlc.types.Field('TeamStatsConnection', graphql_name='teamStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonTypeOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_season', sgqlc.types.Arg(Int, graphql_name='season_season', default=None)),
        ('season_type', sgqlc.types.Arg(SeasonType, graphql_name='seasonType', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
))
    )
    team_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('TeamStats'), graphql_name='teamStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    teams = sgqlc.types.Field('TeamConnection', graphql_name='teams', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(TeamOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='seasonValue', default=None)),
))
    )
    teams_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Team'), graphql_name='teamsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    teams_group = sgqlc.types.Field('TeamsGroup', graphql_name='teamsGroup')
    video = sgqlc.types.Field('Video', graphql_name='video', args=sgqlc.types.ArgDict((
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    video_asset = sgqlc.types.Field('VideoAsset', graphql_name='videoAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    video_assets = sgqlc.types.Field('VideoAssetConnection', graphql_name='videoAssets', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
))
    )
    video_assets_by_ids = sgqlc.types.Field(sgqlc.types.list_of('VideoAsset'), graphql_name='videoAssetsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    videos = sgqlc.types.Field('VideoConnection', graphql_name='videos', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('repository', sgqlc.types.Arg(Repository, graphql_name='repository', default=None)),
        ('order_by', sgqlc.types.Arg(OrderByDates, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('games_id', sgqlc.types.Arg(String, graphql_name='games_id', default=None)),
        ('title_contains', sgqlc.types.Arg(String, graphql_name='titleCONTAINS', default=None)),
        ('last_modified_date_daterange', sgqlc.types.Arg(String, graphql_name='lastModifiedDateDATERANGE', default=None)),
        ('property_id', sgqlc.types.Arg(String, graphql_name='property_id', default=None)),
        ('franchises_id', sgqlc.types.Arg(String, graphql_name='franchises_id', default=None)),
        ('available_to_properties_id', sgqlc.types.Arg(String, graphql_name='availableToProperties_id', default=None)),
        ('video_asset_id_exists', sgqlc.types.Arg(Existence, graphql_name='videoAsset_idEXISTS', default=None)),
))
    )
    videos_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Video'), graphql_name='videosByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    zeppelin_info = sgqlc.types.Field(String, graphql_name='zeppelinInfo')


class SearchGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('search', 'search_autocomplete', 'search_by_tag', 'search_closest_word', 'search_feeling_lucky', 'search_keywords')
    search = sgqlc.types.Field('ShieldSearch', graphql_name='search', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
        ('content_type', sgqlc.types.Arg(sgqlc.types.list_of(ContentType), graphql_name='contentType', default=None)),
        ('order_by', sgqlc.types.Arg(SearchOrderBy, graphql_name='orderBy', default=None)),
))
    )
    search_autocomplete = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='searchAutocomplete', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
))
    )
    search_by_tag = sgqlc.types.Field('ShieldSearch', graphql_name='searchByTag', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('author_id', sgqlc.types.Arg(String, graphql_name='authorId', default=None)),
        ('year', sgqlc.types.Arg(Int, graphql_name='year', default=None)),
        ('month', sgqlc.types.Arg(Int, graphql_name='month', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('content_type', sgqlc.types.Arg(sgqlc.types.list_of(ContentType), graphql_name='contentType', default=None)),
))
    )
    search_closest_word = sgqlc.types.Field(String, graphql_name='searchClosestWord', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
))
    )
    search_feeling_lucky = sgqlc.types.Field('ShieldSearch', graphql_name='searchFeelingLucky', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
        ('query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='query', default=None)),
        ('distance', sgqlc.types.Arg(Int, graphql_name='distance', default=None)),
))
    )
    search_keywords = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='searchKeywords', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='propertyId', default=None)),
))
    )


class SeasonConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SeasonEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class SeasonEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Season'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class SeriesConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SeriesEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class SeriesEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Series'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class ShieldSearch(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('forward', 'limit', 'num_found', 'num_results', 'page', 'query', 'query_closest', 'results', 'used_closest')
    forward = sgqlc.types.Field(Boolean, graphql_name='forward')
    limit = sgqlc.types.Field(Int, graphql_name='limit')
    num_found = sgqlc.types.Field(Int, graphql_name='numFound')
    num_results = sgqlc.types.Field(Long, graphql_name='numResults')
    page = sgqlc.types.Field(Int, graphql_name='page')
    query = sgqlc.types.Field(String, graphql_name='query')
    query_closest = sgqlc.types.Field(String, graphql_name='queryClosest')
    results = sgqlc.types.Field(sgqlc.types.list_of('ShieldSearchResult'), graphql_name='results')
    used_closest = sgqlc.types.Field(Boolean, graphql_name='usedClosest')


class ShowConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ShowEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class ShowEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Show'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class StandingsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('StandingsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class StandingsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Standings'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class StatsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('player_game_stat', 'player_game_stats', 'player_game_stats_by_ids', 'player_stat', 'player_stats', 'player_stats_by_ids', 'player_stats_leaders', 'player_total_career_stats', 'team_game_stat', 'team_game_stats', 'team_game_stats_by_ids', 'team_record_aggregated', 'team_stat', 'team_stats', 'team_stats_by_ids', 'team_stats_leaders')
    player_game_stat = sgqlc.types.Field('PlayerGameStats', graphql_name='playerGameStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_game_stats = sgqlc.types.Field(PlayerGameStatsConnection, graphql_name='playerGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(Int, graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='player_id', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='game_id', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    player_game_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerGameStats'), graphql_name='playerGameStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    player_stat = sgqlc.types.Field('PlayerStats', graphql_name='playerStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_stats = sgqlc.types.Field(PlayerStatsConnection, graphql_name='playerStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonTypeOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_season', sgqlc.types.Arg(Int, graphql_name='season_season', default=None)),
        ('season_type', sgqlc.types.Arg(SeasonType, graphql_name='seasonType', default=None)),
        ('player_id', sgqlc.types.Arg(String, graphql_name='player_id', default=None)),
        ('person_id', sgqlc.types.Arg(String, graphql_name='person_id', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    player_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('PlayerStats'), graphql_name='playerStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    player_stats_leaders = sgqlc.types.Field(PlayerStatsLeadersConnection, graphql_name='playerStatsLeaders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(PlayerStatsLeadersOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
        ('current_team_id', sgqlc.types.Arg(String, graphql_name='currentTeamId', default=None)),
))
    )
    player_total_career_stats = sgqlc.types.Field(sgqlc.types.list_of(PlayerTotalCareerStats), graphql_name='playerTotalCareerStats', args=sgqlc.types.ArgDict((
        ('person_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='person_id', default=None)),
        ('season_type', sgqlc.types.Arg(SeasonType, graphql_name='seasonType', default=None)),
))
    )
    team_game_stat = sgqlc.types.Field('TeamGameStats', graphql_name='teamGameStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    team_game_stats = sgqlc.types.Field('TeamGameStatsConnection', graphql_name='teamGameStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(Int, graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
        ('game_id', sgqlc.types.Arg(String, graphql_name='game_id', default=None)),
))
    )
    team_game_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('TeamGameStats'), graphql_name='teamGameStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    team_record_aggregated = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('TeamRecordAggregated')), graphql_name='teamRecordAggregated', args=sgqlc.types.ArgDict((
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='week_seasonType', default=None)),
        ('week_week_value_lessequal', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_weekValueLESSEQUAL', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
))
    )
    team_stat = sgqlc.types.Field('TeamStats', graphql_name='teamStat', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    team_stats = sgqlc.types.Field('TeamStatsConnection', graphql_name='teamStats', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(SeasonTypeOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_season', sgqlc.types.Arg(Int, graphql_name='season_season', default=None)),
        ('season_type', sgqlc.types.Arg(SeasonType, graphql_name='seasonType', default=None)),
        ('team_id', sgqlc.types.Arg(String, graphql_name='team_id', default=None)),
))
    )
    team_stats_by_ids = sgqlc.types.Field(sgqlc.types.list_of('TeamStats'), graphql_name='teamStatsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    team_stats_leaders = sgqlc.types.Field('TeamStatsLeadersConnection', graphql_name='teamStatsLeaders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(TeamStatsLeaderOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_type', sgqlc.types.Arg(sgqlc.types.non_null(SeasonType), graphql_name='seasonType', default=None)),
        ('season_season', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='season_season', default=None)),
))
    )


class TeamConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('TeamEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class TeamEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Team'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class TeamGameStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('TeamGameStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class TeamGameStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_fumble', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_first_downs', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'redzone_attempts', 'redzone_success', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_fumble = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsFumble')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Int, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    redzone_attempts = sgqlc.types.Field(Int, graphql_name='redzoneAttempts')
    redzone_success = sgqlc.types.Field(Int, graphql_name='redzoneSuccess')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class TeamGameStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('TeamGameStats'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class TeamRecordAggregated(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('record_losses', 'record_ties', 'record_wins', 'team')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    team = sgqlc.types.Field('Team', graphql_name='team')


class TeamSeasonSplitStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_first_downs', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'redzone_attempts', 'redzone_success', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'season_type', 'split_category', 'split_subcategory', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_defense', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_offense', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_special_teams', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Float, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    redzone_attempts = sgqlc.types.Field(Int, graphql_name='redzoneAttempts')
    redzone_success = sgqlc.types.Field(Int, graphql_name='redzoneSuccess')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    split_category = sgqlc.types.Field(String, graphql_name='splitCategory')
    split_subcategory = sgqlc.types.Field(String, graphql_name='splitSubcategory')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_defense = sgqlc.types.Field(Int, graphql_name='touchdownsDefense')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_offense = sgqlc.types.Field(Int, graphql_name='touchdownsOffense')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_special_teams = sgqlc.types.Field(Int, graphql_name='touchdownsSpecialTeams')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class TeamSeasonStatsDetail(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defensive_all_kick_blocked', 'defensive_assists', 'defensive_combine_tackles', 'defensive_fg_blocked', 'defensive_forced_fumble', 'defensive_interceptions', 'defensive_interceptions_avgyds', 'defensive_interceptions_fumble', 'defensive_interceptions_lgtd', 'defensive_interceptions_long', 'defensive_interceptions_tds', 'defensive_interceptions_yards', 'defensive_passes_defensed', 'defensive_punt_blocked', 'defensive_qb_hurries', 'defensive_sacks', 'defensive_safeties', 'defensive_solo_tackles', 'defensive_total_tackles', 'defensive_xp_blocked', 'down1st_attempted', 'down1st_fd_made', 'down2nd_attempted', 'down2nd_fd_made', 'down3rd_attempted', 'down3rd_fd_made', 'down4th_attempted', 'down4th_fd_made', 'extra_point_att1pt_nonkick_hist', 'extra_point_att2pt_nonkick', 'extra_point_good1pt_nonkick_hist', 'extra_point_good2pt_nonkick', 'firstdowns_pass', 'firstdowns_penalty', 'firstdowns_rush', 'firstdowns_total', 'fumbles_aborted_yds', 'fumbles_lost', 'fumbles_outbounds', 'fumbles_safety', 'fumbles_total', 'fumbles_touchback', 'games_dnp', 'games_inactive', 'games_played', 'games_started', 'games_sub', 'kick_returns', 'kick_returns20plus_yards_each', 'kick_returns40plus_yards_each', 'kick_returns_average_yards', 'kick_returns_fair_catches', 'kick_returns_fumbles', 'kick_returns_lgtd', 'kick_returns_long', 'kick_returns_touchdowns', 'kick_returns_yards', 'kicking_fg_att', 'kicking_fg_att_made1_to19', 'kicking_fg_att_made20_to29', 'kicking_fg_att_made30_to39', 'kicking_fg_att_made40_to49', 'kicking_fg_att_made50plus', 'kicking_fg_blk', 'kicking_fg_long', 'kicking_fg_made', 'kicking_fg_pct', 'kicking_xk_att', 'kicking_xk_blk', 'kicking_xk_made', 'kicking_xk_pct', 'kickoff_average_yards', 'kickoff_fair_caught', 'kickoff_onside', 'kickoff_onside_recovered', 'kickoff_outbounds', 'kickoff_returns', 'kickoff_returns_average_yards', 'kickoff_returns_touchdowns', 'kickoff_returns_yards', 'kickoff_total', 'kickoff_touchbacks', 'kickoff_touchbacks_percentage', 'kickoff_yards', 'opponent_fumble_lgtd', 'opponent_fumble_long', 'opponent_fumble_recovery', 'opponent_fumble_td', 'opponent_fumble_yds', 'passing20plus_yards_each', 'passing40plus_yards_each', 'passing_attempts', 'passing_average_yards', 'passing_completion_percentage', 'passing_completions', 'passing_first_down_percentage', 'passing_first_downs', 'passing_fumbles', 'passing_interception_percent', 'passing_interceptions', 'passing_lgtd', 'passing_long', 'passing_net_yards', 'passing_passer_rating', 'passing_sacked', 'passing_sacked_yards_lost', 'passing_touchdown_percentage', 'passing_touchdowns', 'passing_yards', 'penalties_total', 'penalties_yards_penalized', 'punt_returns', 'punt_returns20plus_yards_each', 'punt_returns40plus_yards_each', 'punt_returns_average_yards', 'punt_returns_fair_catches', 'punt_returns_fumbles', 'punt_returns_lgtd', 'punt_returns_long', 'punt_returns_touchdowns', 'punt_returns_yards', 'punting_average_yards', 'punting_blocked', 'punting_downed', 'punting_long', 'punting_net_average', 'punting_net_yardage', 'punting_number_returned', 'punting_out_of_bounds', 'punting_punts', 'punting_punts_fair_caught', 'punting_punts_inside20', 'punting_return_touchdowns', 'punting_return_yards', 'punting_total_punts_incl_blks', 'punting_touchbacks', 'punting_yards', 'receiving20plus_yards_each', 'receiving40plus_yards_each', 'receiving_average_yards', 'receiving_first_down_percent', 'receiving_first_downs', 'receiving_fumbles', 'receiving_lgtd', 'receiving_long', 'receiving_receptions', 'receiving_target', 'receiving_touchdowns', 'receiving_yards', 'receiving_yards_after_catch', 'record_losses', 'record_ties', 'record_win_pct', 'record_wins', 'redzone_attempts', 'redzone_success', 'role', 'rushing20plus_yards_each', 'rushing40plus_yards_each', 'rushing_attempts', 'rushing_average_yards', 'rushing_first_down_percentage', 'rushing_first_downs', 'rushing_fumbles', 'rushing_lgtd', 'rushing_long', 'rushing_touchdowns', 'rushing_yards', 'scrimmage_plays', 'scrimmage_yds', 'season_id', 'season_type', 'team_id', 'teammate_fumble_lgtd', 'teammate_fumble_long', 'teammate_fumble_recovery', 'teammate_fumble_td', 'teammate_fumble_yds', 'time_of_poss_seconds', 'total_points_scored', 'touchdowns_blocked_fg_returns', 'touchdowns_blocked_punt_rtrns', 'touchdowns_fumble_returns', 'touchdowns_interception_rtrns', 'touchdowns_kick_returns', 'touchdowns_ko_rec_in_endzone', 'touchdowns_missed_fg_returns', 'touchdowns_off_lateral_hist', 'touchdowns_passing', 'touchdowns_punt_returns', 'touchdowns_receiving', 'touchdowns_rushing', 'touchdowns_total')
    defensive_all_kick_blocked = sgqlc.types.Field(Int, graphql_name='defensiveAllKickBlocked')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_combine_tackles = sgqlc.types.Field(Int, graphql_name='defensiveCombineTackles')
    defensive_fg_blocked = sgqlc.types.Field(Int, graphql_name='defensiveFgBlocked')
    defensive_forced_fumble = sgqlc.types.Field(Int, graphql_name='defensiveForcedFumble')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_interceptions_avgyds = sgqlc.types.Field(Float, graphql_name='defensiveInterceptionsAvgyds')
    defensive_interceptions_fumble = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsFumble')
    defensive_interceptions_lgtd = sgqlc.types.Field(String, graphql_name='defensiveInterceptionsLgtd')
    defensive_interceptions_long = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsLong')
    defensive_interceptions_tds = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsTds')
    defensive_interceptions_yards = sgqlc.types.Field(Int, graphql_name='defensiveInterceptionsYards')
    defensive_passes_defensed = sgqlc.types.Field(Int, graphql_name='defensivePassesDefensed')
    defensive_punt_blocked = sgqlc.types.Field(Int, graphql_name='defensivePuntBlocked')
    defensive_qb_hurries = sgqlc.types.Field(Int, graphql_name='defensiveQbHurries')
    defensive_sacks = sgqlc.types.Field(Int, graphql_name='defensiveSacks')
    defensive_safeties = sgqlc.types.Field(Int, graphql_name='defensiveSafeties')
    defensive_solo_tackles = sgqlc.types.Field(Int, graphql_name='defensiveSoloTackles')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    defensive_xp_blocked = sgqlc.types.Field(Int, graphql_name='defensiveXpBlocked')
    down1st_attempted = sgqlc.types.Field(Int, graphql_name='down1stAttempted')
    down1st_fd_made = sgqlc.types.Field(Int, graphql_name='down1stFdMade')
    down2nd_attempted = sgqlc.types.Field(Int, graphql_name='down2ndAttempted')
    down2nd_fd_made = sgqlc.types.Field(Int, graphql_name='down2ndFdMade')
    down3rd_attempted = sgqlc.types.Field(Int, graphql_name='down3rdAttempted')
    down3rd_fd_made = sgqlc.types.Field(Int, graphql_name='down3rdFdMade')
    down4th_attempted = sgqlc.types.Field(Int, graphql_name='down4thAttempted')
    down4th_fd_made = sgqlc.types.Field(Int, graphql_name='down4thFdMade')
    extra_point_att1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointAtt1ptNonkickHist')
    extra_point_att2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointAtt2ptNonkick')
    extra_point_good1pt_nonkick_hist = sgqlc.types.Field(Int, graphql_name='extraPointGood1ptNonkickHist')
    extra_point_good2pt_nonkick = sgqlc.types.Field(Int, graphql_name='extraPointGood2ptNonkick')
    firstdowns_pass = sgqlc.types.Field(Int, graphql_name='firstdownsPass')
    firstdowns_penalty = sgqlc.types.Field(Int, graphql_name='firstdownsPenalty')
    firstdowns_rush = sgqlc.types.Field(Int, graphql_name='firstdownsRush')
    firstdowns_total = sgqlc.types.Field(Int, graphql_name='firstdownsTotal')
    fumbles_aborted_yds = sgqlc.types.Field(Int, graphql_name='fumblesAbortedYds')
    fumbles_lost = sgqlc.types.Field(Int, graphql_name='fumblesLost')
    fumbles_outbounds = sgqlc.types.Field(Int, graphql_name='fumblesOutbounds')
    fumbles_safety = sgqlc.types.Field(Int, graphql_name='fumblesSafety')
    fumbles_total = sgqlc.types.Field(Int, graphql_name='fumblesTotal')
    fumbles_touchback = sgqlc.types.Field(Int, graphql_name='fumblesTouchback')
    games_dnp = sgqlc.types.Field(Int, graphql_name='gamesDnp')
    games_inactive = sgqlc.types.Field(Int, graphql_name='gamesInactive')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    games_started = sgqlc.types.Field(Int, graphql_name='gamesStarted')
    games_sub = sgqlc.types.Field(Int, graphql_name='gamesSub')
    kick_returns = sgqlc.types.Field(Int, graphql_name='kickReturns')
    kick_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns20plusYardsEach')
    kick_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='kickReturns40plusYardsEach')
    kick_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickReturnsAverageYards')
    kick_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='kickReturnsFairCatches')
    kick_returns_fumbles = sgqlc.types.Field(Int, graphql_name='kickReturnsFumbles')
    kick_returns_lgtd = sgqlc.types.Field(String, graphql_name='kickReturnsLgtd')
    kick_returns_long = sgqlc.types.Field(Int, graphql_name='kickReturnsLong')
    kick_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickReturnsTouchdowns')
    kick_returns_yards = sgqlc.types.Field(Int, graphql_name='kickReturnsYards')
    kicking_fg_att = sgqlc.types.Field(Int, graphql_name='kickingFgAtt')
    kicking_fg_att_made1_to19 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade1To19')
    kicking_fg_att_made20_to29 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade20To29')
    kicking_fg_att_made30_to39 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade30To39')
    kicking_fg_att_made40_to49 = sgqlc.types.Field(String, graphql_name='kickingFgAttMade40To49')
    kicking_fg_att_made50plus = sgqlc.types.Field(String, graphql_name='kickingFgAttMade50plus')
    kicking_fg_blk = sgqlc.types.Field(Int, graphql_name='kickingFgBlk')
    kicking_fg_long = sgqlc.types.Field(Int, graphql_name='kickingFgLong')
    kicking_fg_made = sgqlc.types.Field(Int, graphql_name='kickingFgMade')
    kicking_fg_pct = sgqlc.types.Field(Float, graphql_name='kickingFgPct')
    kicking_xk_att = sgqlc.types.Field(Int, graphql_name='kickingXkAtt')
    kicking_xk_blk = sgqlc.types.Field(Int, graphql_name='kickingXkBlk')
    kicking_xk_made = sgqlc.types.Field(Int, graphql_name='kickingXkMade')
    kicking_xk_pct = sgqlc.types.Field(Float, graphql_name='kickingXkPct')
    kickoff_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffAverageYards')
    kickoff_fair_caught = sgqlc.types.Field(Int, graphql_name='kickoffFairCaught')
    kickoff_onside = sgqlc.types.Field(Int, graphql_name='kickoffOnside')
    kickoff_onside_recovered = sgqlc.types.Field(Int, graphql_name='kickoffOnsideRecovered')
    kickoff_outbounds = sgqlc.types.Field(Int, graphql_name='kickoffOutbounds')
    kickoff_returns = sgqlc.types.Field(Int, graphql_name='kickoffReturns')
    kickoff_returns_average_yards = sgqlc.types.Field(Float, graphql_name='kickoffReturnsAverageYards')
    kickoff_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='kickoffReturnsTouchdowns')
    kickoff_returns_yards = sgqlc.types.Field(Int, graphql_name='kickoffReturnsYards')
    kickoff_total = sgqlc.types.Field(Int, graphql_name='kickoffTotal')
    kickoff_touchbacks = sgqlc.types.Field(Int, graphql_name='kickoffTouchbacks')
    kickoff_touchbacks_percentage = sgqlc.types.Field(Float, graphql_name='kickoffTouchbacksPercentage')
    kickoff_yards = sgqlc.types.Field(Int, graphql_name='kickoffYards')
    opponent_fumble_lgtd = sgqlc.types.Field(String, graphql_name='opponentFumbleLgtd')
    opponent_fumble_long = sgqlc.types.Field(Int, graphql_name='opponentFumbleLong')
    opponent_fumble_recovery = sgqlc.types.Field(Int, graphql_name='opponentFumbleRecovery')
    opponent_fumble_td = sgqlc.types.Field(Int, graphql_name='opponentFumbleTd')
    opponent_fumble_yds = sgqlc.types.Field(Int, graphql_name='opponentFumbleYds')
    passing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing20plusYardsEach')
    passing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='passing40plusYardsEach')
    passing_attempts = sgqlc.types.Field(Int, graphql_name='passingAttempts')
    passing_average_yards = sgqlc.types.Field(Float, graphql_name='passingAverageYards')
    passing_completion_percentage = sgqlc.types.Field(Float, graphql_name='passingCompletionPercentage')
    passing_completions = sgqlc.types.Field(Int, graphql_name='passingCompletions')
    passing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='passingFirstDownPercentage')
    passing_first_downs = sgqlc.types.Field(Int, graphql_name='passingFirstDowns')
    passing_fumbles = sgqlc.types.Field(Int, graphql_name='passingFumbles')
    passing_interception_percent = sgqlc.types.Field(Float, graphql_name='passingInterceptionPercent')
    passing_interceptions = sgqlc.types.Field(Int, graphql_name='passingInterceptions')
    passing_lgtd = sgqlc.types.Field(String, graphql_name='passingLgtd')
    passing_long = sgqlc.types.Field(Int, graphql_name='passingLong')
    passing_net_yards = sgqlc.types.Field(Int, graphql_name='passingNetYards')
    passing_passer_rating = sgqlc.types.Field(Float, graphql_name='passingPasserRating')
    passing_sacked = sgqlc.types.Field(Int, graphql_name='passingSacked')
    passing_sacked_yards_lost = sgqlc.types.Field(Int, graphql_name='passingSackedYardsLost')
    passing_touchdown_percentage = sgqlc.types.Field(Float, graphql_name='passingTouchdownPercentage')
    passing_touchdowns = sgqlc.types.Field(Int, graphql_name='passingTouchdowns')
    passing_yards = sgqlc.types.Field(Int, graphql_name='passingYards')
    penalties_total = sgqlc.types.Field(Int, graphql_name='penaltiesTotal')
    penalties_yards_penalized = sgqlc.types.Field(Int, graphql_name='penaltiesYardsPenalized')
    punt_returns = sgqlc.types.Field(Int, graphql_name='puntReturns')
    punt_returns20plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns20plusYardsEach')
    punt_returns40plus_yards_each = sgqlc.types.Field(Int, graphql_name='puntReturns40plusYardsEach')
    punt_returns_average_yards = sgqlc.types.Field(Float, graphql_name='puntReturnsAverageYards')
    punt_returns_fair_catches = sgqlc.types.Field(Int, graphql_name='puntReturnsFairCatches')
    punt_returns_fumbles = sgqlc.types.Field(Int, graphql_name='puntReturnsFumbles')
    punt_returns_lgtd = sgqlc.types.Field(String, graphql_name='puntReturnsLgtd')
    punt_returns_long = sgqlc.types.Field(Int, graphql_name='puntReturnsLong')
    punt_returns_touchdowns = sgqlc.types.Field(Int, graphql_name='puntReturnsTouchdowns')
    punt_returns_yards = sgqlc.types.Field(Int, graphql_name='puntReturnsYards')
    punting_average_yards = sgqlc.types.Field(Float, graphql_name='puntingAverageYards')
    punting_blocked = sgqlc.types.Field(Int, graphql_name='puntingBlocked')
    punting_downed = sgqlc.types.Field(Int, graphql_name='puntingDowned')
    punting_long = sgqlc.types.Field(Int, graphql_name='puntingLong')
    punting_net_average = sgqlc.types.Field(Float, graphql_name='puntingNetAverage')
    punting_net_yardage = sgqlc.types.Field(Int, graphql_name='puntingNetYardage')
    punting_number_returned = sgqlc.types.Field(Int, graphql_name='puntingNumberReturned')
    punting_out_of_bounds = sgqlc.types.Field(Int, graphql_name='puntingOutOfBounds')
    punting_punts = sgqlc.types.Field(Int, graphql_name='puntingPunts')
    punting_punts_fair_caught = sgqlc.types.Field(Int, graphql_name='puntingPuntsFairCaught')
    punting_punts_inside20 = sgqlc.types.Field(Int, graphql_name='puntingPuntsInside20')
    punting_return_touchdowns = sgqlc.types.Field(Int, graphql_name='puntingReturnTouchdowns')
    punting_return_yards = sgqlc.types.Field(Int, graphql_name='puntingReturnYards')
    punting_total_punts_incl_blks = sgqlc.types.Field(Int, graphql_name='puntingTotalPuntsInclBlks')
    punting_touchbacks = sgqlc.types.Field(Int, graphql_name='puntingTouchbacks')
    punting_yards = sgqlc.types.Field(Int, graphql_name='puntingYards')
    receiving20plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving20plusYardsEach')
    receiving40plus_yards_each = sgqlc.types.Field(Int, graphql_name='receiving40plusYardsEach')
    receiving_average_yards = sgqlc.types.Field(Float, graphql_name='receivingAverageYards')
    receiving_first_down_percent = sgqlc.types.Field(Float, graphql_name='receivingFirstDownPercent')
    receiving_first_downs = sgqlc.types.Field(Int, graphql_name='receivingFirstDowns')
    receiving_fumbles = sgqlc.types.Field(Int, graphql_name='receivingFumbles')
    receiving_lgtd = sgqlc.types.Field(String, graphql_name='receivingLgtd')
    receiving_long = sgqlc.types.Field(Int, graphql_name='receivingLong')
    receiving_receptions = sgqlc.types.Field(Int, graphql_name='receivingReceptions')
    receiving_target = sgqlc.types.Field(Int, graphql_name='receivingTarget')
    receiving_touchdowns = sgqlc.types.Field(Int, graphql_name='receivingTouchdowns')
    receiving_yards = sgqlc.types.Field(Int, graphql_name='receivingYards')
    receiving_yards_after_catch = sgqlc.types.Field(Int, graphql_name='receivingYardsAfterCatch')
    record_losses = sgqlc.types.Field(Int, graphql_name='recordLosses')
    record_ties = sgqlc.types.Field(Int, graphql_name='recordTies')
    record_win_pct = sgqlc.types.Field(Float, graphql_name='recordWinPct')
    record_wins = sgqlc.types.Field(Int, graphql_name='recordWins')
    redzone_attempts = sgqlc.types.Field(Int, graphql_name='redzoneAttempts')
    redzone_success = sgqlc.types.Field(Int, graphql_name='redzoneSuccess')
    role = sgqlc.types.Field(String, graphql_name='role')
    rushing20plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing20plusYardsEach')
    rushing40plus_yards_each = sgqlc.types.Field(Int, graphql_name='rushing40plusYardsEach')
    rushing_attempts = sgqlc.types.Field(Int, graphql_name='rushingAttempts')
    rushing_average_yards = sgqlc.types.Field(Float, graphql_name='rushingAverageYards')
    rushing_first_down_percentage = sgqlc.types.Field(Float, graphql_name='rushingFirstDownPercentage')
    rushing_first_downs = sgqlc.types.Field(Int, graphql_name='rushingFirstDowns')
    rushing_fumbles = sgqlc.types.Field(Int, graphql_name='rushingFumbles')
    rushing_lgtd = sgqlc.types.Field(String, graphql_name='rushingLgtd')
    rushing_long = sgqlc.types.Field(Int, graphql_name='rushingLong')
    rushing_touchdowns = sgqlc.types.Field(Int, graphql_name='rushingTouchdowns')
    rushing_yards = sgqlc.types.Field(Int, graphql_name='rushingYards')
    scrimmage_plays = sgqlc.types.Field(Int, graphql_name='scrimmagePlays')
    scrimmage_yds = sgqlc.types.Field(Int, graphql_name='scrimmageYds')
    season_id = sgqlc.types.Field(Int, graphql_name='seasonId')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')
    teammate_fumble_lgtd = sgqlc.types.Field(String, graphql_name='teammateFumbleLgtd')
    teammate_fumble_long = sgqlc.types.Field(Int, graphql_name='teammateFumbleLong')
    teammate_fumble_recovery = sgqlc.types.Field(Int, graphql_name='teammateFumbleRecovery')
    teammate_fumble_td = sgqlc.types.Field(Int, graphql_name='teammateFumbleTd')
    teammate_fumble_yds = sgqlc.types.Field(Int, graphql_name='teammateFumbleYds')
    time_of_poss_seconds = sgqlc.types.Field(Int, graphql_name='timeOfPossSeconds')
    total_points_scored = sgqlc.types.Field(Int, graphql_name='totalPointsScored')
    touchdowns_blocked_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedFgReturns')
    touchdowns_blocked_punt_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsBlockedPuntRtrns')
    touchdowns_fumble_returns = sgqlc.types.Field(Int, graphql_name='touchdownsFumbleReturns')
    touchdowns_interception_rtrns = sgqlc.types.Field(Int, graphql_name='touchdownsInterceptionRtrns')
    touchdowns_kick_returns = sgqlc.types.Field(Int, graphql_name='touchdownsKickReturns')
    touchdowns_ko_rec_in_endzone = sgqlc.types.Field(Int, graphql_name='touchdownsKoRecInEndzone')
    touchdowns_missed_fg_returns = sgqlc.types.Field(Int, graphql_name='touchdownsMissedFgReturns')
    touchdowns_off_lateral_hist = sgqlc.types.Field(Int, graphql_name='touchdownsOffLateralHist')
    touchdowns_passing = sgqlc.types.Field(Int, graphql_name='touchdownsPassing')
    touchdowns_punt_returns = sgqlc.types.Field(Int, graphql_name='touchdownsPuntReturns')
    touchdowns_receiving = sgqlc.types.Field(Int, graphql_name='touchdownsReceiving')
    touchdowns_rushing = sgqlc.types.Field(Int, graphql_name='touchdownsRushing')
    touchdowns_total = sgqlc.types.Field(Int, graphql_name='touchdownsTotal')


class TeamStatsConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('TeamStatsEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class TeamStatsEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('TeamStats'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class TeamStatsLeaders(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('defense_passing_net_yards', 'defense_passing_net_yards_per_game', 'defense_rushing_yards', 'defense_rushing_yards_per_game', 'defense_scrimmage_yds', 'defense_scrimmage_yds_per_game', 'defensive_assists', 'defensive_interceptions', 'defensive_sacks', 'defensive_total_tackles', 'games_played', 'offense_passing_net_yards', 'offense_passing_net_yards_per_game', 'offense_rushing_yards', 'offense_rushing_yards_per_game', 'offense_scrimmage_yds', 'offense_scrimmage_yds_per_game', 'team', 'total_tackles')
    defense_passing_net_yards = sgqlc.types.Field(Int, graphql_name='defensePassingNetYards')
    defense_passing_net_yards_per_game = sgqlc.types.Field(Float, graphql_name='defensePassingNetYardsPerGame')
    defense_rushing_yards = sgqlc.types.Field(Int, graphql_name='defenseRushingYards')
    defense_rushing_yards_per_game = sgqlc.types.Field(Float, graphql_name='defenseRushingYardsPerGame')
    defense_scrimmage_yds = sgqlc.types.Field(Int, graphql_name='defenseScrimmageYds')
    defense_scrimmage_yds_per_game = sgqlc.types.Field(Float, graphql_name='defenseScrimmageYdsPerGame')
    defensive_assists = sgqlc.types.Field(Int, graphql_name='defensiveAssists')
    defensive_interceptions = sgqlc.types.Field(Int, graphql_name='defensiveInterceptions')
    defensive_sacks = sgqlc.types.Field(Int, graphql_name='defensiveSacks')
    defensive_total_tackles = sgqlc.types.Field(Float, graphql_name='defensiveTotalTackles')
    games_played = sgqlc.types.Field(Int, graphql_name='gamesPlayed')
    offense_passing_net_yards = sgqlc.types.Field(Int, graphql_name='offensePassingNetYards')
    offense_passing_net_yards_per_game = sgqlc.types.Field(Float, graphql_name='offensePassingNetYardsPerGame')
    offense_rushing_yards = sgqlc.types.Field(Int, graphql_name='offenseRushingYards')
    offense_rushing_yards_per_game = sgqlc.types.Field(Float, graphql_name='offenseRushingYardsPerGame')
    offense_scrimmage_yds = sgqlc.types.Field(Int, graphql_name='offenseScrimmageYds')
    offense_scrimmage_yds_per_game = sgqlc.types.Field(Float, graphql_name='offenseScrimmageYdsPerGame')
    team = sgqlc.types.Field('Team', graphql_name='team')
    total_tackles = sgqlc.types.Field(Float, graphql_name='totalTackles')


class TeamStatsLeadersConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('TeamStatsLeadersEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class TeamStatsLeadersEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(TeamStatsLeaders, graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class TeamsGroup(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('franchise', 'franchises', 'franchises_by_ids', 'player_team', 'player_teams', 'standing', 'standings', 'standings_by_ids', 'team', 'teams', 'teams_by_franchise', 'teams_by_ids', 'teams_on_bye')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    franchises = sgqlc.types.Field(FranchiseConnection, graphql_name='franchises', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(FranchiseOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('state', sgqlc.types.Arg(FranchiseState, graphql_name='state', default=None)),
))
    )
    franchises_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Franchise'), graphql_name='franchisesByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    player_team = sgqlc.types.Field(PlayerTeam, graphql_name='playerTeam', args=sgqlc.types.ArgDict((
        ('player_team_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='playerTeamId', default=None)),
))
    )
    player_teams = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(PlayerTeam)), graphql_name='playerTeams', args=sgqlc.types.ArgDict((
        ('esb_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='esbId', default=None)),
        ('season_value', sgqlc.types.Arg(Int, graphql_name='seasonValue', default=None)),
))
    )
    standing = sgqlc.types.Field('Standings', graphql_name='standing', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    standings = sgqlc.types.Field(StandingsConnection, graphql_name='standings', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(WeekOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('week_season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='week_seasonValue', default=None)),
        ('week_season_type', sgqlc.types.Arg(SeasonType, graphql_name='week_seasonType', default=None)),
        ('week_week_value', sgqlc.types.Arg(Int, graphql_name='week_weekValue', default=None)),
))
    )
    standings_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Standings'), graphql_name='standingsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    team = sgqlc.types.Field('Team', graphql_name='team', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    teams = sgqlc.types.Field(TeamConnection, graphql_name='teams', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('order_by', sgqlc.types.Arg(TeamOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='seasonValue', default=None)),
))
    )
    teams_by_franchise = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Team')), graphql_name='teamsByFranchise', args=sgqlc.types.ArgDict((
        ('order_by', sgqlc.types.Arg(TeamOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
        ('franchise_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='franchise_id', default=None)),
        ('season_value', sgqlc.types.Arg(Int, graphql_name='seasonValue', default=None)),
))
    )
    teams_by_ids = sgqlc.types.Field(sgqlc.types.list_of('Team'), graphql_name='teamsByIds', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(ID)), graphql_name='ids', default=None)),
))
    )
    teams_on_bye = sgqlc.types.Field(sgqlc.types.list_of('TeamOnBye'), graphql_name='teamsOnBye', args=sgqlc.types.ArgDict((
        ('season_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='seasonValue', default=None)),
        ('week_value', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='weekValue', default=None)),
))
    )


class TimeSeriesCount(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('keys', 'time')
    keys = sgqlc.types.Field(sgqlc.types.list_of(Key), graphql_name='keys')
    time = sgqlc.types.Field(String, graphql_name='time')


class TotalCount(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('count', 'key', 'percentage')
    count = sgqlc.types.Field(Long, graphql_name='count')
    key = sgqlc.types.Field(String, graphql_name='key')
    percentage = sgqlc.types.Field(Float, graphql_name='percentage')


class VideoAssetConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('VideoAssetEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class VideoAssetEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('VideoAsset'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class VideoConnection(sgqlc.types.relay.Connection):
    __schema__ = shield
    __field_names__ = ('edges', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('VideoEdge'), graphql_name='edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfoWithTotal), graphql_name='pageInfo')


class VideoEdge(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('node', 'cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Video'), graphql_name='node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')


class Viewer(sgqlc.types.Type):
    __schema__ = shield
    __field_names__ = ('viewer',)
    viewer = sgqlc.types.Field(Root, graphql_name='viewer')


class Article(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('author', 'elements', 'html_body_url', 'image', 'markdown_body', 'mobile_headline', 'series_list', 'short_headline', 'video', 'web_url')
    author = sgqlc.types.Field('AuthorPerson', graphql_name='author')
    elements = sgqlc.types.Field(AbstractEntityConnection, graphql_name='elements', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
))
    )
    html_body_url = sgqlc.types.Field(String, graphql_name='htmlBodyUrl')
    image = sgqlc.types.Field('Image', graphql_name='image')
    markdown_body = sgqlc.types.Field(String, graphql_name='markdownBody')
    mobile_headline = sgqlc.types.Field(String, graphql_name='mobileHeadline')
    series_list = sgqlc.types.Field(sgqlc.types.list_of('Series'), graphql_name='seriesList')
    short_headline = sgqlc.types.Field(String, graphql_name='shortHeadline')
    video = sgqlc.types.Field('Video', graphql_name='video')
    web_url = sgqlc.types.Field(String, graphql_name='webUrl')


class Audio(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('audio_asset', 'event_occurred_date', 'image', 'series_list')
    audio_asset = sgqlc.types.Field('AudioAsset', graphql_name='audioAsset')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    image = sgqlc.types.Field('Image', graphql_name='image')
    series_list = sgqlc.types.Field(sgqlc.types.list_of('Series'), graphql_name='seriesList')


class AudioAsset(sgqlc.types.Type, AbstractAsset, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('bitrates', 'closed_captions_url', 'encoding_date', 'image', 'music', 'playback_url', 'playback_url2', 'runtime_secs', 'closed_captions_embedded')
    bitrates = sgqlc.types.Field(sgqlc.types.list_of('Bitrate'), graphql_name='bitrates')
    closed_captions_url = sgqlc.types.Field(String, graphql_name='closedCaptionsUrl')
    encoding_date = sgqlc.types.Field(DateTime, graphql_name='encodingDate')
    image = sgqlc.types.Field('Image', graphql_name='image')
    music = sgqlc.types.Field(sgqlc.types.list_of(Music), graphql_name='music')
    playback_url = sgqlc.types.Field(String, graphql_name='playbackUrl')
    playback_url2 = sgqlc.types.Field(String, graphql_name='playbackUrl2')
    runtime_secs = sgqlc.types.Field(Int, graphql_name='runtimeSecs')
    closed_captions_embedded = sgqlc.types.Field(Boolean, graphql_name='closedCaptionsEmbedded')


class AuthorPerson(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('awards', 'byline', 'headshot', 'hire_day', 'hire_month', 'hire_year', 'meta_data', 'person', 'property', 'slug', 'socials', 'work_status')
    awards = sgqlc.types.Field(sgqlc.types.list_of(Award), graphql_name='awards')
    byline = sgqlc.types.Field(String, graphql_name='byline')
    headshot = sgqlc.types.Field('Image', graphql_name='headshot')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    property = sgqlc.types.Field('Property', graphql_name='property')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class Bitrate(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('bitrate_kbps', 'filename', 'remote_path')
    bitrate_kbps = sgqlc.types.Field(Int, graphql_name='bitrateKbps')
    filename = sgqlc.types.Field(String, graphql_name='filename')
    remote_path = sgqlc.types.Field(String, graphql_name='remotePath')


class BlackListPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('black_list',)
    black_list = sgqlc.types.Field(BlackList, graphql_name='blackList')


class CelebrationPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('celebration',)
    celebration = sgqlc.types.Field(Celebration, graphql_name='celebration')


class Cheerleader(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('cheerleader_person', 'current_team', 'eye_color', 'hair_color', 'hire_day', 'hire_month', 'hire_year', 'nfl_experience', 'occupation', 'person', 'season', 'season_value', 'tenure', 'title', 'title_description', 'work_status')
    cheerleader_person = sgqlc.types.Field('CheerleaderPerson', graphql_name='cheerleaderPerson')
    current_team = sgqlc.types.Field('Team', graphql_name='currentTeam')
    eye_color = sgqlc.types.Field(String, graphql_name='eyeColor')
    hair_color = sgqlc.types.Field(String, graphql_name='hairColor')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    occupation = sgqlc.types.Field(String, graphql_name='occupation')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CheerleaderPerson(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('awards', 'cheerleaders', 'eye_color', 'hair_color', 'headshot', 'hire_day', 'hire_month', 'hire_year', 'large_image', 'link_page', 'meta_data', 'nfl_experience', 'occupation', 'property', 'slug', 'socials', 'tenure', 'work_status')
    awards = sgqlc.types.Field(sgqlc.types.list_of(Award), graphql_name='awards')
    cheerleaders = sgqlc.types.Field(AbstractEntityConnection, graphql_name='cheerleaders', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
))
    )
    eye_color = sgqlc.types.Field(String, graphql_name='eyeColor')
    hair_color = sgqlc.types.Field(String, graphql_name='hairColor')
    headshot = sgqlc.types.Field('Image', graphql_name='headshot')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    large_image = sgqlc.types.Field('Image', graphql_name='largeImage')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    occupation = sgqlc.types.Field(String, graphql_name='occupation')
    property = sgqlc.types.Field('Property', graphql_name='property')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')
    tenure = sgqlc.types.Field(String, graphql_name='tenure')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class ClearIdentityProviderGroupPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('identity_providers',)
    identity_providers = sgqlc.types.Field(sgqlc.types.list_of('IdentityProvider'), graphql_name='identityProviders')


class ClubInjury(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('display_name', 'headshot_image_url', 'injuries', 'injury_status', 'player_id', 'position', 'practice_statuses', 'practices', 'season_type', 'season_value', 'team_id', 'week_value')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    headshot_image_url = sgqlc.types.Field(String, graphql_name='headshotImageUrl')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='injuries')
    injury_status = sgqlc.types.Field(InjuryStatus, graphql_name='injuryStatus')
    player_id = sgqlc.types.Field(String, graphql_name='playerId')
    position = sgqlc.types.Field(String, graphql_name='position')
    practice_statuses = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practiceStatuses')
    practices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practices')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')
    week_value = sgqlc.types.Field(Int, graphql_name='weekValue')


class ClubTransaction(sgqlc.types.Type, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('franchise', 'transaction_day', 'transaction_detail', 'transaction_month', 'transaction_year')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    transaction_day = sgqlc.types.Field(Int, graphql_name='transactionDay')
    transaction_detail = sgqlc.types.Field(String, graphql_name='transactionDetail')
    transaction_month = sgqlc.types.Field(Int, graphql_name='transactionMonth')
    transaction_year = sgqlc.types.Field(Int, graphql_name='transactionYear')


class Coach(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('coach_person', 'current_team', 'hire_day', 'hire_month', 'hire_year', 'nfl_experience', 'person', 'season', 'season_value', 'tenure', 'title', 'title_description', 'unit', 'work_status')
    coach_person = sgqlc.types.Field('CoachPerson', graphql_name='coachPerson')
    current_team = sgqlc.types.Field('Team', graphql_name='currentTeam')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')
    unit = sgqlc.types.Field(Platoon, graphql_name='unit')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CoachPerson(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('awards', 'coach_type', 'coaches', 'headshot', 'hire_day', 'hire_month', 'hire_year', 'link_page', 'meta_data', 'nfl_experience', 'property', 'slug', 'socials', 'work_status')
    awards = sgqlc.types.Field(sgqlc.types.list_of(Award), graphql_name='awards')
    coach_type = sgqlc.types.Field(CoachType, graphql_name='coachType')
    coaches = sgqlc.types.Field(sgqlc.types.list_of(Coach), graphql_name='coaches', args=sgqlc.types.ArgDict((
        ('order_by', sgqlc.types.Arg(CoachOrderBy, graphql_name='orderBy', default=None)),
        ('order_by_direction', sgqlc.types.Arg(OrderByDirection, graphql_name='orderByDirection', default=None)),
))
    )
    headshot = sgqlc.types.Field('Image', graphql_name='headshot')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    property = sgqlc.types.Field('Property', graphql_name='property')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class CoinToss(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('before_quarter', 'losing_choice', 'winning_choice', 'winning_team_id')
    before_quarter = sgqlc.types.Field(Int, graphql_name='beforeQuarter')
    losing_choice = sgqlc.types.Field(String, graphql_name='losingChoice')
    winning_choice = sgqlc.types.Field(String, graphql_name='winningChoice')
    winning_team_id = sgqlc.types.Field(String, graphql_name='winningTeamId')


class CommonIdentityProviderGroupPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('identity_provider_group',)
    identity_provider_group = sgqlc.types.Field('IdentityProviderGroup', graphql_name='identityProviderGroup')


class CommonIdentityProviderPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('identity_provider',)
    identity_provider = sgqlc.types.Field('IdentityProvider', graphql_name='identityProvider')


class CommonVoidPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('result',)
    result = sgqlc.types.Field(String, graphql_name='result')


class Content(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('content_type', 'last_modified', 'season', 'summary', 'tags', 'title', 'url')
    content_type = sgqlc.types.Field(ContentType, graphql_name='contentType')
    last_modified = sgqlc.types.Field(DateTime, graphql_name='lastModified')
    season = sgqlc.types.Field(Int, graphql_name='season')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(String, graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')


class ContentList(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('authors', 'content_hints', 'content_list_type', 'contents', 'curation', 'external_id', 'image', 'materialization_hint', 'series_list', 'aggregate')
    authors = sgqlc.types.Field(sgqlc.types.list_of(AuthorPerson), graphql_name='authors')
    content_hints = sgqlc.types.Field(sgqlc.types.list_of(ContentHint), graphql_name='contentHints')
    content_list_type = sgqlc.types.Field(ContentHint, graphql_name='contentListType')
    contents = sgqlc.types.Field(AbstractContentConnection, graphql_name='contents', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('type', sgqlc.types.Arg(ContentHint, graphql_name='type', default=None)),
))
    )
    curation = sgqlc.types.Field(Curation, graphql_name='curation')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    image = sgqlc.types.Field('Image', graphql_name='image')
    materialization_hint = sgqlc.types.Field(MaterializationHint, graphql_name='materializationHint')
    series_list = sgqlc.types.Field(sgqlc.types.list_of('Series'), graphql_name='seriesList')
    aggregate = sgqlc.types.Field(Boolean, graphql_name='aggregate')


class CreateArticlePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('article',)
    article = sgqlc.types.Field(Article, graphql_name='article')


class CreateAudioAssetPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('audio_asset',)
    audio_asset = sgqlc.types.Field(AudioAsset, graphql_name='audioAsset')


class CreateAudioPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('audio',)
    audio = sgqlc.types.Field(Audio, graphql_name='audio')


class CreateAuthorPersonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('author',)
    author = sgqlc.types.Field(AuthorPerson, graphql_name='author')


class CreateCheerleaderPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('cheerleader',)
    cheerleader = sgqlc.types.Field(Cheerleader, graphql_name='cheerleader')


class CreateCheerleaderPersonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('cheerleader_person',)
    cheerleader_person = sgqlc.types.Field(CheerleaderPerson, graphql_name='cheerleaderPerson')


class CreateClubInjuryReportPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('club_injury_report',)
    club_injury_report = sgqlc.types.Field(ClubInjury, graphql_name='clubInjuryReport')


class CreateClubTransactionPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('club_transaction',)
    club_transaction = sgqlc.types.Field(ClubTransaction, graphql_name='clubTransaction')


class CreateCoachPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('coach',)
    coach = sgqlc.types.Field(Coach, graphql_name='coach')


class CreateCoachPersonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('coach_person',)
    coach_person = sgqlc.types.Field(CoachPerson, graphql_name='coachPerson')


class CreateContentListPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('content_list',)
    content_list = sgqlc.types.Field(ContentList, graphql_name='contentList')


class CreateCurrentClubDepthChartPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('current_club_depth_chart',)
    current_club_depth_chart = sgqlc.types.Field('CurrentClubDepthChart', graphql_name='currentClubDepthChart')


class CreateCurrentClubRosterPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('current_club_roster',)
    current_club_roster = sgqlc.types.Field('CurrentClubRoster', graphql_name='currentClubRoster')


class CreateCurrentContextualPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('current_contextual',)
    current_contextual = sgqlc.types.Field('CurrentContextual', graphql_name='currentContextual')


class CreateDepthChartPositionOrderPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('depth_chart_position_order',)
    depth_chart_position_order = sgqlc.types.Field('DepthChartPositionOrder', graphql_name='depthChartPositionOrder')


class CreateDraftPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('draft',)
    draft = sgqlc.types.Field('Draft', graphql_name='draft')


class CreateDraftPickPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('draft_pick',)
    draft_pick = sgqlc.types.Field(DraftPick, graphql_name='draftPick')


class CreateDraftTeamPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('draft_team',)
    draft_team = sgqlc.types.Field('DraftTeam', graphql_name='draftTeam')


class CreateEventPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('event',)
    event = sgqlc.types.Field('Event', graphql_name='event')


class CreateExecutivePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('executive',)
    executive = sgqlc.types.Field('Executive', graphql_name='executive')


class CreateExecutivePersonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('executive_person',)
    executive_person = sgqlc.types.Field('ExecutivePerson', graphql_name='executivePerson')


class CreateGamePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('game',)
    game = sgqlc.types.Field('Game', graphql_name='game')


class CreateImageAssetPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('image_asset',)
    image_asset = sgqlc.types.Field('ImageAsset', graphql_name='imageAsset')


class CreateImagePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('image',)
    image = sgqlc.types.Field('Image', graphql_name='image')


class CreateInjuryReportPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('injury_report',)
    injury_report = sgqlc.types.Field('Injury', graphql_name='injuryReport')


class CreateMetaPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('metas',)
    metas = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metas')


class CreateMilestonePlayerPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'game_detail_id', 'gsis_player_id', 'milestone_type', 'milestone_value')
    current_team_id = sgqlc.types.Field(String, graphql_name='currentTeamId')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    gsis_player_id = sgqlc.types.Field(String, graphql_name='gsisPlayerId')
    milestone_type = sgqlc.types.Field(MilestoneType, graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(Int, graphql_name='milestoneValue')


class CreateMilestoneTeamPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'milestone_type', 'milestone_value', 'team_id')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    milestone_type = sgqlc.types.Field(MilestoneType, graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(Int, graphql_name='milestoneValue')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')


class CreateMockDraftPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('mock_draft',)
    mock_draft = sgqlc.types.Field('MockDraft', graphql_name='mockDraft')


class CreateMockDraftPickPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('mock_draft_pick',)
    mock_draft_pick = sgqlc.types.Field('MockDraftPick', graphql_name='mockDraftPick')


class CreatePersonListPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('person_list',)
    person_list = sgqlc.types.Field('PersonList', graphql_name='personList')


class CreatePromoPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('promo',)
    promo = sgqlc.types.Field('Promo', graphql_name='promo')


class CreateProspectPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('prospect',)
    prospect = sgqlc.types.Field('Prospect', graphql_name='prospect')


class CreateSeasonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('season',)
    season = sgqlc.types.Field('Season', graphql_name='season')


class CreateSeriesPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('series',)
    series = sgqlc.types.Field('Series', graphql_name='series')


class CreateShowPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('show',)
    show = sgqlc.types.Field('Show', graphql_name='show')


class CreateTagPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('tag',)
    tag = sgqlc.types.Field('Tag', graphql_name='tag')


class CreateTeamPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('team',)
    team = sgqlc.types.Field('Team', graphql_name='team')


class CreateVideoAssetPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('video_asset',)
    video_asset = sgqlc.types.Field('VideoAsset', graphql_name='videoAsset')


class CreateVideoPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('video',)
    video = sgqlc.types.Field('Video', graphql_name='video')


class CreateWeekPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('week',)
    week = sgqlc.types.Field('Week', graphql_name='week')


class Current(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('season', 'season_value', 'week')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    week = sgqlc.types.Field('Week', graphql_name='week')


class CurrentClubDepthChart(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('depth_num', 'depth_num_label', 'display_name', 'first_name', 'last_name', 'person_id', 'platoon', 'platoon_label', 'position', 'position_label', 'property_id')
    depth_num = sgqlc.types.Field(Float, graphql_name='depthNum')
    depth_num_label = sgqlc.types.Field(String, graphql_name='depthNumLabel')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    person_id = sgqlc.types.Field(String, graphql_name='personId')
    platoon = sgqlc.types.Field(Platoon, graphql_name='platoon')
    platoon_label = sgqlc.types.Field(String, graphql_name='platoonLabel')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_label = sgqlc.types.Field(String, graphql_name='positionLabel')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')


class CurrentClubRoster(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('birth_day', 'birth_month', 'birth_year', 'college', 'display_name', 'first_name', 'headshot_image_url', 'height', 'jersey_number', 'last_name', 'nfl_experience', 'person', 'person_id', 'position', 'property_id', 'status', 'weight')
    birth_day = sgqlc.types.Field(Int, graphql_name='birthDay')
    birth_month = sgqlc.types.Field(Int, graphql_name='birthMonth')
    birth_year = sgqlc.types.Field(Int, graphql_name='birthYear')
    college = sgqlc.types.Field(String, graphql_name='college')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    headshot_image_url = sgqlc.types.Field(String, graphql_name='headshotImageUrl')
    height = sgqlc.types.Field(String, graphql_name='height')
    jersey_number = sgqlc.types.Field(Int, graphql_name='jerseyNumber')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    person_id = sgqlc.types.Field(String, graphql_name='personId')
    position = sgqlc.types.Field(String, graphql_name='position')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')
    status = sgqlc.types.Field(String, graphql_name='status')
    weight = sgqlc.types.Field(Int, graphql_name='weight')


class CurrentContextual(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('context', 'type', 'value')
    context = sgqlc.types.Field(CurrentContext, graphql_name='context')
    type = sgqlc.types.Field(CurrentType, graphql_name='type')
    value = sgqlc.types.Field(String, graphql_name='value')


class DepthChartPositionOrder(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('position_order', 'property_id')
    position_order = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='positionOrder')
    property_id = sgqlc.types.Field(String, graphql_name='propertyId')


class Draft(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('complete', 'current_pick', 'current_round', 'draft_state', 'name', 'picks', 'team_on_the_clock', 'venue', 'year')
    complete = sgqlc.types.Field(Boolean, graphql_name='complete')
    current_pick = sgqlc.types.Field(Int, graphql_name='currentPick')
    current_round = sgqlc.types.Field(Int, graphql_name='currentRound')
    draft_state = sgqlc.types.Field(DraftState, graphql_name='draftState')
    name = sgqlc.types.Field(String, graphql_name='name')
    picks = sgqlc.types.Field(sgqlc.types.list_of(DraftPick), graphql_name='picks')
    team_on_the_clock = sgqlc.types.Field('DraftTeam', graphql_name='teamOnTheClock')
    venue = sgqlc.types.Field('Venue', graphql_name='venue')
    year = sgqlc.types.Field(Int, graphql_name='year')


class DraftTeam(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('franchise', 'grade', 'needs', 'needs_by_position_cb', 'needs_by_position_dl', 'needs_by_position_lb', 'needs_by_position_ol', 'needs_by_position_qb', 'needs_by_position_rb', 'needs_by_position_spec', 'needs_by_position_te', 'needs_by_position_wr', 'notes', 'position_needs', 'post_draft_assessment', 'ticket_url', 'year')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    grade = sgqlc.types.Field(String, graphql_name='grade')
    needs = sgqlc.types.Field(Int, graphql_name='needs')
    needs_by_position_cb = sgqlc.types.Field(Int, graphql_name='needsByPositionCB')
    needs_by_position_dl = sgqlc.types.Field(Int, graphql_name='needsByPositionDL')
    needs_by_position_lb = sgqlc.types.Field(Int, graphql_name='needsByPositionLB')
    needs_by_position_ol = sgqlc.types.Field(Int, graphql_name='needsByPositionOL')
    needs_by_position_qb = sgqlc.types.Field(Int, graphql_name='needsByPositionQB')
    needs_by_position_rb = sgqlc.types.Field(Int, graphql_name='needsByPositionRB')
    needs_by_position_spec = sgqlc.types.Field(Int, graphql_name='needsByPositionSpec')
    needs_by_position_te = sgqlc.types.Field(Int, graphql_name='needsByPositionTE')
    needs_by_position_wr = sgqlc.types.Field(Int, graphql_name='needsByPositionWR')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    position_needs = sgqlc.types.Field(String, graphql_name='positionNeeds')
    post_draft_assessment = sgqlc.types.Field(String, graphql_name='postDraftAssessment')
    ticket_url = sgqlc.types.Field(String, graphql_name='ticketUrl')
    year = sgqlc.types.Field(Int, graphql_name='year')


class Drive(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('end_transition', 'end_yard_line', 'ended_with_score', 'first_downs', 'game_clock_end', 'game_clock_start', 'game_detail_id', 'gsis_id', 'how_ended_description', 'how_started_description', 'inside20', 'order_sequence', 'play_count', 'play_id_ended', 'play_id_started', 'play_seq_ended', 'play_seq_started', 'possession_team', 'quarter_end', 'quarter_start', 'real_start_time', 'start_transition', 'start_yard_line', 'time_of_possession', 'total_ended_with_score', 'yards', 'yards_penalized')
    end_transition = sgqlc.types.Field(Transition, graphql_name='endTransition')
    end_yard_line = sgqlc.types.Field(String, graphql_name='endYardLine')
    ended_with_score = sgqlc.types.Field(Boolean, graphql_name='endedWithScore')
    first_downs = sgqlc.types.Field(Int, graphql_name='firstDowns')
    game_clock_end = sgqlc.types.Field(String, graphql_name='gameClockEnd')
    game_clock_start = sgqlc.types.Field(String, graphql_name='gameClockStart')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    how_ended_description = sgqlc.types.Field(String, graphql_name='howEndedDescription')
    how_started_description = sgqlc.types.Field(String, graphql_name='howStartedDescription')
    inside20 = sgqlc.types.Field(Boolean, graphql_name='inside20')
    order_sequence = sgqlc.types.Field(Int, graphql_name='orderSequence')
    play_count = sgqlc.types.Field(Int, graphql_name='playCount')
    play_id_ended = sgqlc.types.Field(Int, graphql_name='playIdEnded')
    play_id_started = sgqlc.types.Field(Int, graphql_name='playIdStarted')
    play_seq_ended = sgqlc.types.Field(Int, graphql_name='playSeqEnded')
    play_seq_started = sgqlc.types.Field(Int, graphql_name='playSeqStarted')
    possession_team = sgqlc.types.Field('Team', graphql_name='possessionTeam')
    quarter_end = sgqlc.types.Field(Int, graphql_name='quarterEnd')
    quarter_start = sgqlc.types.Field(Int, graphql_name='quarterStart')
    real_start_time = sgqlc.types.Field(String, graphql_name='realStartTime')
    start_transition = sgqlc.types.Field(Transition, graphql_name='startTransition')
    start_yard_line = sgqlc.types.Field(String, graphql_name='startYardLine')
    time_of_possession = sgqlc.types.Field(String, graphql_name='timeOfPossession')
    total_ended_with_score = sgqlc.types.Field(Boolean, graphql_name='totalEndedWithScore')
    yards = sgqlc.types.Field(Int, graphql_name='yards')
    yards_penalized = sgqlc.types.Field(Int, graphql_name='yardsPenalized')


class EliasCollege(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('created_date', 'last_modified_date', 'name', 'state')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    name = sgqlc.types.Field(String, graphql_name='name')
    state = sgqlc.types.Field(String, graphql_name='state')


class EliasPlayerGameStats(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('game', 'game_stats', 'person', 'player', 'season_value')
    game = sgqlc.types.Field('Game', graphql_name='game')
    game_stats = sgqlc.types.Field(EliasStatsDetail, graphql_name='gameStats')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    player = sgqlc.types.Field('Player', graphql_name='player')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')


class EliasPlayerTeamStats(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('franchise', 'person', 'person_team_stats', 'player', 'season_type', 'season_value', 'team')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    person_team_stats = sgqlc.types.Field(EliasStatsDetail, graphql_name='personTeamStats')
    player = sgqlc.types.Field('Player', graphql_name='player')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team = sgqlc.types.Field('Team', graphql_name='team')


class EliasPosition(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('description', 'position')
    description = sgqlc.types.Field(String, graphql_name='description')
    position = sgqlc.types.Field(String, graphql_name='position')


class EliasTeam(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('abbr', 'full_name', 'nick')
    abbr = sgqlc.types.Field(String, graphql_name='abbr')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    nick = sgqlc.types.Field(String, graphql_name='nick')


class EliasTeamStats(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('franchise', 'season_type', 'season_value', 'team', 'team_stats')
    franchise = sgqlc.types.Field('Franchise', graphql_name='franchise')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_stats = sgqlc.types.Field(EliasStatsDetail, graphql_name='teamStats')


class Event(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('active', 'audio', 'cta_button_text', 'cta_link', 'cta_second_button_text', 'cta_second_link', 'days_of_week', 'end_date', 'end_time', 'event_type', 'image', 'location', 'location_url', 'name', 'online', 'recurrence', 'start_date', 'start_time', 'video')
    active = sgqlc.types.Field(Boolean, graphql_name='active')
    audio = sgqlc.types.Field(Audio, graphql_name='audio')
    cta_button_text = sgqlc.types.Field(String, graphql_name='ctaButtonText')
    cta_link = sgqlc.types.Field(String, graphql_name='ctaLink')
    cta_second_button_text = sgqlc.types.Field(String, graphql_name='ctaSecondButtonText')
    cta_second_link = sgqlc.types.Field(String, graphql_name='ctaSecondLink')
    days_of_week = sgqlc.types.Field(sgqlc.types.list_of(DayOfWeek), graphql_name='daysOfWeek')
    end_date = sgqlc.types.Field(DateTime, graphql_name='endDate')
    end_time = sgqlc.types.Field(DateTime, graphql_name='endTime')
    event_type = sgqlc.types.Field(EventType, graphql_name='eventType')
    image = sgqlc.types.Field('Image', graphql_name='image')
    location = sgqlc.types.Field(String, graphql_name='location')
    location_url = sgqlc.types.Field(String, graphql_name='locationUrl')
    name = sgqlc.types.Field(String, graphql_name='name')
    online = sgqlc.types.Field(Boolean, graphql_name='online')
    recurrence = sgqlc.types.Field(Recurrence, graphql_name='recurrence')
    start_date = sgqlc.types.Field(DateTime, graphql_name='startDate')
    start_time = sgqlc.types.Field(DateTime, graphql_name='startTime')
    video = sgqlc.types.Field('Video', graphql_name='video')


class Executive(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('current_team', 'department', 'executive_person', 'hire_day', 'hire_month', 'hire_year', 'nfl_experience', 'person', 'season', 'season_value', 'tenure', 'title', 'title_description', 'work_status')
    current_team = sgqlc.types.Field('Team', graphql_name='currentTeam')
    department = sgqlc.types.Field(String, graphql_name='department')
    executive_person = sgqlc.types.Field('ExecutivePerson', graphql_name='executivePerson')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    tenure = sgqlc.types.Field(Int, graphql_name='tenure')
    title = sgqlc.types.Field(String, graphql_name='title')
    title_description = sgqlc.types.Field(String, graphql_name='titleDescription')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class ExecutivePerson(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('awards', 'executives', 'headshot', 'hire_day', 'hire_month', 'hire_year', 'link_page', 'meta_data', 'nfl_experience', 'property', 'slug', 'socials', 'work_status')
    awards = sgqlc.types.Field(sgqlc.types.list_of(Award), graphql_name='awards')
    executives = sgqlc.types.Field(sgqlc.types.list_of(Executive), graphql_name='executives')
    headshot = sgqlc.types.Field('Image', graphql_name='headshot')
    hire_day = sgqlc.types.Field(Int, graphql_name='hireDay')
    hire_month = sgqlc.types.Field(Int, graphql_name='hireMonth')
    hire_year = sgqlc.types.Field(Int, graphql_name='hireYear')
    link_page = sgqlc.types.Field(Boolean, graphql_name='linkPage')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    property = sgqlc.types.Field('Property', graphql_name='property')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')
    work_status = sgqlc.types.Field(WorkStatus, graphql_name='workStatus')


class Franchise(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('current_background', 'current_logo', 'current_team', 'current_team_bio', 'first_season', 'name', 'nfl_shop_url', 'official_website_url', 'owner', 'primary_color', 'property', 'secondary_color', 'slug', 'socials', 'state', 'teams', 'year_established')
    current_background = sgqlc.types.Field('Image', graphql_name='currentBackground')
    current_logo = sgqlc.types.Field('Image', graphql_name='currentLogo')
    current_team = sgqlc.types.Field('Team', graphql_name='currentTeam')
    current_team_bio = sgqlc.types.Field(String, graphql_name='currentTeamBio')
    first_season = sgqlc.types.Field(Int, graphql_name='firstSeason')
    name = sgqlc.types.Field(String, graphql_name='name')
    nfl_shop_url = sgqlc.types.Field(String, graphql_name='nflShopUrl')
    official_website_url = sgqlc.types.Field(String, graphql_name='officialWebsiteUrl')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    primary_color = sgqlc.types.Field(String, graphql_name='primaryColor')
    property = sgqlc.types.Field('Property', graphql_name='property')
    secondary_color = sgqlc.types.Field(String, graphql_name='secondaryColor')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')
    state = sgqlc.types.Field(FranchiseState, graphql_name='state')
    teams = sgqlc.types.Field(sgqlc.types.list_of('Team'), graphql_name='teams')
    year_established = sgqlc.types.Field(Int, graphql_name='yearEstablished')


class Game(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('away_team', 'category', 'esb_id', 'game_detail_id', 'game_time', 'gsis_id', 'home_team', 'network_channels', 'radio_links', 'slug', 'territory', 'ticket_url', 'venue', 'week')
    away_team = sgqlc.types.Field('Team', graphql_name='awayTeam')
    category = sgqlc.types.Field(String, graphql_name='category')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    game_time = sgqlc.types.Field(DateTime, graphql_name='gameTime')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    home_team = sgqlc.types.Field('Team', graphql_name='homeTeam')
    network_channels = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='networkChannels')
    radio_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='radioLinks')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    territory = sgqlc.types.Field(String, graphql_name='territory')
    ticket_url = sgqlc.types.Field(String, graphql_name='ticketUrl')
    venue = sgqlc.types.Field('Venue', graphql_name='venue')
    week = sgqlc.types.Field('Week', graphql_name='week')


class GameDetail(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('attendance', 'back_judge', 'coin_toss_results', 'coin_toss_winner', 'current_event_id', 'distance', 'down', 'drives', 'field_judge', 'file_number', 'game_clock', 'game_injuries', 'game_key', 'game_refresh', 'game_time', 'goal_to_go', 'head_linesman', 'home_head_coach', 'home_live_game_roster', 'home_points_overtime', 'home_points_overtime_total', 'home_points_q1', 'home_points_q2', 'home_points_q3', 'home_points_q4', 'home_points_total', 'home_team', 'home_timeouts_remaining', 'home_timeouts_used', 'line_judge', 'live_home_player_game_stats', 'live_home_team_game_stats', 'live_visitor_player_game_stats', 'live_visitor_team_game_stats', 'period', 'phase', 'play_review', 'play_review_play_id', 'plays', 'possession_team', 'redzone', 'referee', 'replay_official', 'scoring_summaries', 'side_judge', 'stadium', 'start_time', 'umpire', 'visitor_head_coach', 'visitor_live_game_roster', 'visitor_points_overtime', 'visitor_points_overtime_total', 'visitor_points_q1', 'visitor_points_q2', 'visitor_points_q3', 'visitor_points_q4', 'visitor_points_total', 'visitor_team', 'visitor_timeouts_remaining', 'visitor_timeouts_used', 'weather', 'yard_line', 'yards_to_go')
    attendance = sgqlc.types.Field(String, graphql_name='attendance')
    back_judge = sgqlc.types.Field(String, graphql_name='backJudge')
    coin_toss_results = sgqlc.types.Field(sgqlc.types.list_of(CoinToss), graphql_name='coinTossResults')
    coin_toss_winner = sgqlc.types.Field('Team', graphql_name='coinTossWinner')
    current_event_id = sgqlc.types.Field(String, graphql_name='currentEventId')
    distance = sgqlc.types.Field(Int, graphql_name='distance')
    down = sgqlc.types.Field(Int, graphql_name='down')
    drives = sgqlc.types.Field(sgqlc.types.list_of(Drive), graphql_name='drives')
    field_judge = sgqlc.types.Field(String, graphql_name='fieldJudge')
    file_number = sgqlc.types.Field(Int, graphql_name='fileNumber')
    game_clock = sgqlc.types.Field(String, graphql_name='gameClock')
    game_injuries = sgqlc.types.Field(sgqlc.types.list_of('GameInjury'), graphql_name='gameInjuries')
    game_key = sgqlc.types.Field(String, graphql_name='gameKey')
    game_refresh = sgqlc.types.Field(String, graphql_name='gameRefresh')
    game_time = sgqlc.types.Field(DateTime, graphql_name='gameTime')
    goal_to_go = sgqlc.types.Field(Boolean, graphql_name='goalToGo')
    head_linesman = sgqlc.types.Field(String, graphql_name='headLinesman')
    home_head_coach = sgqlc.types.Field(String, graphql_name='homeHeadCoach')
    home_live_game_roster = sgqlc.types.Field(sgqlc.types.list_of('LiveGameRoster'), graphql_name='homeLiveGameRoster')
    home_points_overtime = sgqlc.types.Field(Int, graphql_name='homePointsOvertime')
    home_points_overtime_total = sgqlc.types.Field(Int, graphql_name='homePointsOvertimeTotal')
    home_points_q1 = sgqlc.types.Field(Int, graphql_name='homePointsQ1')
    home_points_q2 = sgqlc.types.Field(Int, graphql_name='homePointsQ2')
    home_points_q3 = sgqlc.types.Field(Int, graphql_name='homePointsQ3')
    home_points_q4 = sgqlc.types.Field(Int, graphql_name='homePointsQ4')
    home_points_total = sgqlc.types.Field(Int, graphql_name='homePointsTotal')
    home_team = sgqlc.types.Field('Team', graphql_name='homeTeam')
    home_timeouts_remaining = sgqlc.types.Field(Int, graphql_name='homeTimeoutsRemaining')
    home_timeouts_used = sgqlc.types.Field(Int, graphql_name='homeTimeoutsUsed')
    line_judge = sgqlc.types.Field(String, graphql_name='lineJudge')
    live_home_player_game_stats = sgqlc.types.Field(sgqlc.types.list_of('LivePlayerGameStats'), graphql_name='liveHomePlayerGameStats')
    live_home_team_game_stats = sgqlc.types.Field('LiveTeamGameStats', graphql_name='liveHomeTeamGameStats')
    live_visitor_player_game_stats = sgqlc.types.Field(sgqlc.types.list_of('LivePlayerGameStats'), graphql_name='liveVisitorPlayerGameStats')
    live_visitor_team_game_stats = sgqlc.types.Field('LiveTeamGameStats', graphql_name='liveVisitorTeamGameStats')
    period = sgqlc.types.Field(Int, graphql_name='period')
    phase = sgqlc.types.Field(Phase, graphql_name='phase')
    play_review = sgqlc.types.Field(Boolean, graphql_name='playReview')
    play_review_play_id = sgqlc.types.Field(Int, graphql_name='playReviewPlayId')
    plays = sgqlc.types.Field(sgqlc.types.list_of('Play'), graphql_name='plays')
    possession_team = sgqlc.types.Field('Team', graphql_name='possessionTeam')
    redzone = sgqlc.types.Field(Boolean, graphql_name='redzone')
    referee = sgqlc.types.Field(String, graphql_name='referee')
    replay_official = sgqlc.types.Field(String, graphql_name='replayOfficial')
    scoring_summaries = sgqlc.types.Field(sgqlc.types.list_of('ScoringSummary'), graphql_name='scoringSummaries')
    side_judge = sgqlc.types.Field(String, graphql_name='sideJudge')
    stadium = sgqlc.types.Field(String, graphql_name='stadium')
    start_time = sgqlc.types.Field(String, graphql_name='startTime')
    umpire = sgqlc.types.Field(String, graphql_name='umpire')
    visitor_head_coach = sgqlc.types.Field(String, graphql_name='visitorHeadCoach')
    visitor_live_game_roster = sgqlc.types.Field(sgqlc.types.list_of('LiveGameRoster'), graphql_name='visitorLiveGameRoster')
    visitor_points_overtime = sgqlc.types.Field(Int, graphql_name='visitorPointsOvertime')
    visitor_points_overtime_total = sgqlc.types.Field(Int, graphql_name='visitorPointsOvertimeTotal')
    visitor_points_q1 = sgqlc.types.Field(Int, graphql_name='visitorPointsQ1')
    visitor_points_q2 = sgqlc.types.Field(Int, graphql_name='visitorPointsQ2')
    visitor_points_q3 = sgqlc.types.Field(Int, graphql_name='visitorPointsQ3')
    visitor_points_q4 = sgqlc.types.Field(Int, graphql_name='visitorPointsQ4')
    visitor_points_total = sgqlc.types.Field(Int, graphql_name='visitorPointsTotal')
    visitor_team = sgqlc.types.Field('Team', graphql_name='visitorTeam')
    visitor_timeouts_remaining = sgqlc.types.Field(Int, graphql_name='visitorTimeoutsRemaining')
    visitor_timeouts_used = sgqlc.types.Field(Int, graphql_name='visitorTimeoutsUsed')
    weather = sgqlc.types.Field('Weather', graphql_name='weather')
    yard_line = sgqlc.types.Field(String, graphql_name='yardLine')
    yards_to_go = sgqlc.types.Field(Int, graphql_name='yardsToGo')


class GameInjury(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'gsis_player', 'gsis_player_id', 'play_id', 'player_name', 'return_status', 'team', 'uniform_number')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    gsis_player = sgqlc.types.Field('GsisPlayer', graphql_name='gsisPlayer')
    gsis_player_id = sgqlc.types.Field(String, graphql_name='gsisPlayerId')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')
    player_name = sgqlc.types.Field(String, graphql_name='playerName')
    return_status = sgqlc.types.Field(String, graphql_name='returnStatus')
    team = sgqlc.types.Field('Team', graphql_name='team')
    uniform_number = sgqlc.types.Field(String, graphql_name='uniformNumber')


class GameInsight(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('game_id', 'headline', 'insight', 'insight_type', 'is_evergreen', 'items', 'label')
    game_id = sgqlc.types.Field(String, graphql_name='gameId')
    headline = sgqlc.types.Field(String, graphql_name='headline')
    insight = sgqlc.types.Field(String, graphql_name='insight')
    insight_type = sgqlc.types.Field(InsightTemplate, graphql_name='insightType')
    is_evergreen = sgqlc.types.Field(Boolean, graphql_name='isEvergreen')
    items = sgqlc.types.Field(sgqlc.types.list_of(InsightItem), graphql_name='items')
    label = sgqlc.types.Field(String, graphql_name='label')


class GameInsightPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('game_insight',)
    game_insight = sgqlc.types.Field(GameInsight, graphql_name='gameInsight')


class GenerateSmartIDPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('generate_smart_id',)
    generate_smart_id = sgqlc.types.Field(GeneratedSmartID, graphql_name='generateSmartID')


class GsisPlayer(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('entry_year', 'height', 'person', 'position', 'rookie_year', 'weight')
    entry_year = sgqlc.types.Field(Int, graphql_name='entryYear')
    height = sgqlc.types.Field(String, graphql_name='height')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    position = sgqlc.types.Field(String, graphql_name='position')
    rookie_year = sgqlc.types.Field(Int, graphql_name='rookieYear')
    weight = sgqlc.types.Field(Int, graphql_name='weight')


class HeimdallrPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('heimdallr_response',)
    heimdallr_response = sgqlc.types.Field(HeimdallrResponse, graphql_name='heimdallrResponse')


class IdentityProvider(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('adobe_mso_id', 'app_url_android', 'app_url_ios', 'auth_provider_id', 'display_name', 'display_order', 'enabled', 'identity_provider_group_ids', 'logo_url', 'max_streams', 'name', 'tms_mso_id', 'type', 'website')
    adobe_mso_id = sgqlc.types.Field(String, graphql_name='adobeMsoId')
    app_url_android = sgqlc.types.Field(String, graphql_name='appUrlAndroid')
    app_url_ios = sgqlc.types.Field(String, graphql_name='appUrlIos')
    auth_provider_id = sgqlc.types.Field(String, graphql_name='authProviderId')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    display_order = sgqlc.types.Field(Int, graphql_name='displayOrder')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')
    identity_provider_group_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='identityProviderGroupIds')
    logo_url = sgqlc.types.Field(String, graphql_name='logoUrl')
    max_streams = sgqlc.types.Field(Int, graphql_name='maxStreams')
    name = sgqlc.types.Field(String, graphql_name='name')
    tms_mso_id = sgqlc.types.Field(String, graphql_name='tmsMsoId')
    type = sgqlc.types.Field(String, graphql_name='type')
    website = sgqlc.types.Field(String, graphql_name='website')


class IdentityProviderGroup(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('auth_provider_id', 'identity_provider_ids', 'logo_url', 'name', 'priority')
    auth_provider_id = sgqlc.types.Field(String, graphql_name='authProviderId')
    identity_provider_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='identityProviderIds')
    logo_url = sgqlc.types.Field(String, graphql_name='logoUrl')
    name = sgqlc.types.Field(String, graphql_name='name')
    priority = sgqlc.types.Field(Int, graphql_name='priority')


class Image(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('asset', 'attribution', 'author_byline', 'copyright', 'external_id', 'file_name', 'for_purchase', 'image_type', 'photographer_name', 'play', 'url')
    asset = sgqlc.types.Field('ImageAsset', graphql_name='asset')
    attribution = sgqlc.types.Field(String, graphql_name='attribution')
    author_byline = sgqlc.types.Field(String, graphql_name='authorByline')
    copyright = sgqlc.types.Field(String, graphql_name='copyright')
    external_id = sgqlc.types.Field(String, graphql_name='externalId')
    file_name = sgqlc.types.Field(String, graphql_name='fileName')
    for_purchase = sgqlc.types.Field(ForPurchase, graphql_name='forPurchase')
    image_type = sgqlc.types.Field(ImageType, graphql_name='imageType')
    photographer_name = sgqlc.types.Field(String, graphql_name='photographerName')
    play = sgqlc.types.Field('Play', graphql_name='play')
    url = sgqlc.types.Field(String, graphql_name='url')


class ImageAsset(sgqlc.types.Type, AbstractAsset, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('author_byline', 'camera_make', 'camera_model', 'caption', 'copyright', 'file_name', 'file_size', 'format', 'hash_sum', 'height', 'photographer_name', 'shutter_speed', 'software', 'subject_distance', 'title', 'width')
    author_byline = sgqlc.types.Field(String, graphql_name='authorByline')
    camera_make = sgqlc.types.Field(String, graphql_name='cameraMake')
    camera_model = sgqlc.types.Field(String, graphql_name='cameraModel')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    copyright = sgqlc.types.Field(String, graphql_name='copyright')
    file_name = sgqlc.types.Field(String, graphql_name='fileName')
    file_size = sgqlc.types.Field(Long, graphql_name='fileSize')
    format = sgqlc.types.Field(String, graphql_name='format')
    hash_sum = sgqlc.types.Field(String, graphql_name='hashSum')
    height = sgqlc.types.Field(Int, graphql_name='height')
    photographer_name = sgqlc.types.Field(String, graphql_name='photographerName')
    shutter_speed = sgqlc.types.Field(Float, graphql_name='shutterSpeed')
    software = sgqlc.types.Field(String, graphql_name='software')
    subject_distance = sgqlc.types.Field(Float, graphql_name='subjectDistance')
    title = sgqlc.types.Field(String, graphql_name='title')
    width = sgqlc.types.Field(Int, graphql_name='width')


class InjuredPlayer(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('display_name', 'headshot', 'injuries', 'injury_status', 'player_id', 'position', 'practice_statuses', 'practices')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    headshot = sgqlc.types.Field(Image, graphql_name='headshot')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='injuries')
    injury_status = sgqlc.types.Field(InjuryStatus, graphql_name='injuryStatus')
    player_id = sgqlc.types.Field(String, graphql_name='playerId')
    position = sgqlc.types.Field(String, graphql_name='position')
    practice_statuses = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practiceStatuses')
    practices = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='practices')


class Injury(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('club_reported_injuries', 'league_reported_injuries', 'team', 'week')
    club_reported_injuries = sgqlc.types.Field(sgqlc.types.list_of(InjuredPlayer), graphql_name='clubReportedInjuries')
    league_reported_injuries = sgqlc.types.Field(sgqlc.types.list_of(InjuredPlayer), graphql_name='leagueReportedInjuries')
    team = sgqlc.types.Field('Team', graphql_name='team')
    week = sgqlc.types.Field('Week', graphql_name='week')


class LeagueTransaction(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('date', 'date_loaded', 'date_voided', 'day', 'description', 'description_abbr', 'dst_franchise', 'dst_status_desc', 'month', 'player_person', 'season_value', 'src_franchise', 'src_status_desc', 'status', 'transaction_id', 'year')
    date = sgqlc.types.Field(DateTime, graphql_name='date')
    date_loaded = sgqlc.types.Field(DateTime, graphql_name='dateLoaded')
    date_voided = sgqlc.types.Field(DateTime, graphql_name='dateVoided')
    day = sgqlc.types.Field(Int, graphql_name='day')
    description = sgqlc.types.Field(String, graphql_name='description')
    description_abbr = sgqlc.types.Field(String, graphql_name='descriptionAbbr')
    dst_franchise = sgqlc.types.Field(Franchise, graphql_name='dstFranchise')
    dst_status_desc = sgqlc.types.Field(String, graphql_name='dstStatusDesc')
    month = sgqlc.types.Field(Int, graphql_name='month')
    player_person = sgqlc.types.Field('PlayerPerson', graphql_name='playerPerson')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    src_franchise = sgqlc.types.Field(Franchise, graphql_name='srcFranchise')
    src_status_desc = sgqlc.types.Field(String, graphql_name='srcStatusDesc')
    status = sgqlc.types.Field(Long, graphql_name='status')
    transaction_id = sgqlc.types.Field(Long, graphql_name='transactionId')
    year = sgqlc.types.Field(Int, graphql_name='year')


class LiveGameRoster(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('first_name', 'gsis_player', 'jersey_number', 'last_name', 'position', 'season_id', 'status')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    gsis_player = sgqlc.types.Field(GsisPlayer, graphql_name='gsisPlayer')
    jersey_number = sgqlc.types.Field(String, graphql_name='jerseyNumber')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    position = sgqlc.types.Field(String, graphql_name='position')
    season_id = sgqlc.types.Field(Int, graphql_name='seasonId')
    status = sgqlc.types.Field(LiveGameRosterStatus, graphql_name='status')


class LivePlayerGameStats(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('game_detail', 'game_stats', 'player', 'team')
    game_detail = sgqlc.types.Field(GameDetail, graphql_name='gameDetail')
    game_stats = sgqlc.types.Field(PlayerGameStatsDetail, graphql_name='gameStats')
    player = sgqlc.types.Field(GsisPlayer, graphql_name='player')
    team = sgqlc.types.Field('Team', graphql_name='team')


class LiveTeamGameStats(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('game_detail', 'team', 'team_game_stats')
    game_detail = sgqlc.types.Field(GameDetail, graphql_name='gameDetail')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_game_stats = sgqlc.types.Field(TeamGameStatsDetail, graphql_name='teamGameStats')


class MediaToken(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('token',)
    token = sgqlc.types.Field(String, graphql_name='token')


class MilestoneTeam(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'milestone_type', 'milestone_value', 'team', 'team_game_stats')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    milestone_type = sgqlc.types.Field(MilestoneType, graphql_name='milestoneType')
    milestone_value = sgqlc.types.Field(Int, graphql_name='milestoneValue')
    team = sgqlc.types.Field('Team', graphql_name='team')
    team_game_stats = sgqlc.types.Field(LiveTeamGameStats, graphql_name='teamGameStats')


class MockDraft(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('author', 'caption', 'draft_picks', 'title', 'version', 'video', 'year')
    author = sgqlc.types.Field(AuthorPerson, graphql_name='author')
    caption = sgqlc.types.Field(String, graphql_name='caption')
    draft_picks = sgqlc.types.Field(sgqlc.types.list_of('MockDraftPick'), graphql_name='draftPicks')
    title = sgqlc.types.Field(String, graphql_name='title')
    version = sgqlc.types.Field(String, graphql_name='version')
    video = sgqlc.types.Field('Video', graphql_name='video')
    year = sgqlc.types.Field(Int, graphql_name='year')


class MockDraftPick(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('analysis', 'franchise', 'pick_number', 'prospect')
    analysis = sgqlc.types.Field(String, graphql_name='analysis')
    franchise = sgqlc.types.Field(Franchise, graphql_name='franchise')
    pick_number = sgqlc.types.Field(Int, graphql_name='pickNumber')
    prospect = sgqlc.types.Field('Prospect', graphql_name='prospect')


class PersonList(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('image', 'materialization_hint', 'person_ids')
    image = sgqlc.types.Field(Image, graphql_name='image')
    materialization_hint = sgqlc.types.Field(MaterializationHint, graphql_name='materializationHint')
    person_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='personIds')


class Play(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('clock_time', 'down', 'drive_net_yards', 'drive_play_count', 'drive_sequence_number', 'drive_time_of_possession', 'end_clock_time', 'end_quarter_play', 'end_yard_line', 'first_down', 'game_detail_id', 'goal_to_go', 'gsis_id', 'is_big_play', 'next_play_is_goal_to_go', 'next_play_type', 'order_sequence', 'penalty_on_play', 'play_clock', 'play_deleted', 'play_description', 'play_description_with_jersey_numbers', 'play_id', 'play_review_status', 'play_stats', 'play_type', 'possession_team', 'pre_play_by_play', 'quarter', 'scoring_play', 'scoring_play_type', 'scoring_team', 'short_description', 'special_teams_play', 'st_play_type', 'time_of_day', 'time_of_day_as_date', 'yard_line', 'yards', 'yards_to_go', 'latest_play')
    clock_time = sgqlc.types.Field(String, graphql_name='clockTime')
    down = sgqlc.types.Field(Int, graphql_name='down')
    drive_net_yards = sgqlc.types.Field(Int, graphql_name='driveNetYards')
    drive_play_count = sgqlc.types.Field(Int, graphql_name='drivePlayCount')
    drive_sequence_number = sgqlc.types.Field(Int, graphql_name='driveSequenceNumber')
    drive_time_of_possession = sgqlc.types.Field(String, graphql_name='driveTimeOfPossession')
    end_clock_time = sgqlc.types.Field(String, graphql_name='endClockTime')
    end_quarter_play = sgqlc.types.Field(Boolean, graphql_name='endQuarterPlay')
    end_yard_line = sgqlc.types.Field(String, graphql_name='endYardLine')
    first_down = sgqlc.types.Field(Boolean, graphql_name='firstDown')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    goal_to_go = sgqlc.types.Field(Boolean, graphql_name='goalToGo')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    is_big_play = sgqlc.types.Field(Boolean, graphql_name='isBigPlay')
    next_play_is_goal_to_go = sgqlc.types.Field(Boolean, graphql_name='nextPlayIsGoalToGo')
    next_play_type = sgqlc.types.Field(PlayType, graphql_name='nextPlayType')
    order_sequence = sgqlc.types.Field(Float, graphql_name='orderSequence')
    penalty_on_play = sgqlc.types.Field(Boolean, graphql_name='penaltyOnPlay')
    play_clock = sgqlc.types.Field(String, graphql_name='playClock')
    play_deleted = sgqlc.types.Field(Boolean, graphql_name='playDeleted')
    play_description = sgqlc.types.Field(String, graphql_name='playDescription')
    play_description_with_jersey_numbers = sgqlc.types.Field(String, graphql_name='playDescriptionWithJerseyNumbers')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')
    play_review_status = sgqlc.types.Field(PlayReviewStatus, graphql_name='playReviewStatus')
    play_stats = sgqlc.types.Field(sgqlc.types.list_of('PlayStats'), graphql_name='playStats')
    play_type = sgqlc.types.Field(PlayType, graphql_name='playType')
    possession_team = sgqlc.types.Field('Team', graphql_name='possessionTeam')
    pre_play_by_play = sgqlc.types.Field(String, graphql_name='prePlayByPlay')
    quarter = sgqlc.types.Field(Int, graphql_name='quarter')
    scoring_play = sgqlc.types.Field(Boolean, graphql_name='scoringPlay')
    scoring_play_type = sgqlc.types.Field(ScoringPlayType, graphql_name='scoringPlayType')
    scoring_team = sgqlc.types.Field('Team', graphql_name='scoringTeam')
    short_description = sgqlc.types.Field(String, graphql_name='shortDescription')
    special_teams_play = sgqlc.types.Field(Boolean, graphql_name='specialTeamsPlay')
    st_play_type = sgqlc.types.Field(PlayType, graphql_name='stPlayType')
    time_of_day = sgqlc.types.Field(String, graphql_name='timeOfDay')
    time_of_day_as_date = sgqlc.types.Field(DateTime, graphql_name='timeOfDayAsDate')
    yard_line = sgqlc.types.Field(String, graphql_name='yardLine')
    yards = sgqlc.types.Field(Int, graphql_name='yards')
    yards_to_go = sgqlc.types.Field(Int, graphql_name='yardsToGo')
    latest_play = sgqlc.types.Field(Boolean, graphql_name='latestPlay')


class PlayStats(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('game_detail_id', 'gsis_player', 'play_id', 'play_stat_seq', 'player_name', 'stat_id', 'team', 'uniform_number', 'yards')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    gsis_player = sgqlc.types.Field(GsisPlayer, graphql_name='gsisPlayer')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')
    play_stat_seq = sgqlc.types.Field(Int, graphql_name='playStatSeq')
    player_name = sgqlc.types.Field(String, graphql_name='playerName')
    stat_id = sgqlc.types.Field(Int, graphql_name='statId')
    team = sgqlc.types.Field('Team', graphql_name='team')
    uniform_number = sgqlc.types.Field(String, graphql_name='uniformNumber')
    yards = sgqlc.types.Field(Int, graphql_name='yards')


class Player(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('acquired_day', 'acquired_from_id', 'acquired_month', 'acquired_year', 'acquisition_type', 'current_team', 'esb_id', 'gsis_id', 'height', 'jersey_number', 'meta_data', 'nfl_experience', 'person', 'position', 'position_group', 'season', 'season_value', 'status', 'teams', 'weight')
    acquired_day = sgqlc.types.Field(Int, graphql_name='acquiredDay')
    acquired_from_id = sgqlc.types.Field(String, graphql_name='acquiredFromId')
    acquired_month = sgqlc.types.Field(Int, graphql_name='acquiredMonth')
    acquired_year = sgqlc.types.Field(Int, graphql_name='acquiredYear')
    acquisition_type = sgqlc.types.Field(String, graphql_name='acquisitionType')
    current_team = sgqlc.types.Field('Team', graphql_name='currentTeam')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    height = sgqlc.types.Field(String, graphql_name='height')
    jersey_number = sgqlc.types.Field(String, graphql_name='jerseyNumber')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    nfl_experience = sgqlc.types.Field(Int, graphql_name='nflExperience')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_group = sgqlc.types.Field(PositionGroup, graphql_name='positionGroup')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    status = sgqlc.types.Field(Status, graphql_name='status')
    teams = sgqlc.types.Field(sgqlc.types.list_of('Team'), graphql_name='teams')
    weight = sgqlc.types.Field(Int, graphql_name='weight')


class PlayerAward(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('award_description', 'award_type', 'person', 'player', 'season_value')
    award_description = sgqlc.types.Field(String, graphql_name='awardDescription')
    award_type = sgqlc.types.Field(String, graphql_name='awardType')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    player = sgqlc.types.Field(Player, graphql_name='player')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')


class PlayerGameStats(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'game', 'game_stats', 'person', 'player', 'season', 'season_value', 'week')
    current_team_id = sgqlc.types.Field(String, graphql_name='currentTeamId')
    game = sgqlc.types.Field(Game, graphql_name='game')
    game_stats = sgqlc.types.Field(PlayerGameStatsDetail, graphql_name='gameStats')
    person = sgqlc.types.Field('PlayerPerson', graphql_name='person')
    player = sgqlc.types.Field(Player, graphql_name='player')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    week = sgqlc.types.Field('Week', graphql_name='week')


class PlayerPerson(sgqlc.types.Type, AbstractPerson, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('action_shot', 'all_profiles', 'awards', 'birth_city', 'birth_country', 'birth_state_prov', 'current_player', 'current_profile', 'draft_number_overall', 'draft_player_position', 'draft_position', 'draft_round', 'draft_team', 'draft_type', 'draft_year', 'elias_home_country', 'esb_id', 'gsis_id', 'headshot', 'meta_data', 'players', 'property', 'slug', 'socials')
    action_shot = sgqlc.types.Field(Image, graphql_name='actionShot')
    all_profiles = sgqlc.types.Field(sgqlc.types.list_of(ProfileType), graphql_name='allProfiles')
    awards = sgqlc.types.Field(sgqlc.types.list_of(Award), graphql_name='awards')
    birth_city = sgqlc.types.Field(String, graphql_name='birthCity')
    birth_country = sgqlc.types.Field(String, graphql_name='birthCountry')
    birth_state_prov = sgqlc.types.Field(String, graphql_name='birthStateProv')
    current_player = sgqlc.types.Field(Player, graphql_name='currentPlayer')
    current_profile = sgqlc.types.Field(ProfileType, graphql_name='currentProfile')
    draft_number_overall = sgqlc.types.Field(Int, graphql_name='draftNumberOverall')
    draft_player_position = sgqlc.types.Field(String, graphql_name='draftPlayerPosition')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_team = sgqlc.types.Field('Team', graphql_name='draftTeam')
    draft_type = sgqlc.types.Field(String, graphql_name='draftType')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    elias_home_country = sgqlc.types.Field(String, graphql_name='eliasHomeCountry')
    esb_id = sgqlc.types.Field(String, graphql_name='esbId')
    gsis_id = sgqlc.types.Field(String, graphql_name='gsisId')
    headshot = sgqlc.types.Field(Image, graphql_name='headshot')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    players = sgqlc.types.Field(sgqlc.types.list_of(Player), graphql_name='players')
    property = sgqlc.types.Field('Property', graphql_name='property')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    socials = sgqlc.types.Field(sgqlc.types.list_of('Social'), graphql_name='socials')


class PlayerStats(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('current_team_id', 'person', 'player', 'season', 'season_stats', 'season_type', 'season_value', 'split_stats', 'team_stats')
    current_team_id = sgqlc.types.Field(String, graphql_name='currentTeamId')
    person = sgqlc.types.Field(PlayerPerson, graphql_name='person')
    player = sgqlc.types.Field(Player, graphql_name='player')
    season = sgqlc.types.Field('Season', graphql_name='season')
    season_stats = sgqlc.types.Field(PlayerSeasonStatsDetail, graphql_name='seasonStats')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    split_stats = sgqlc.types.Field(sgqlc.types.list_of(PlayerSeasonSplitStatsDetail), graphql_name='splitStats')
    team_stats = sgqlc.types.Field(sgqlc.types.list_of(PlayerTeamStatsDetail), graphql_name='teamStats')


class Promo(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('background_image', 'content_category', 'cta_button_text', 'cta_link', 'cta_second_button_text', 'cta_second_link', 'image', 'url')
    background_image = sgqlc.types.Field(Image, graphql_name='backgroundImage')
    content_category = sgqlc.types.Field(String, graphql_name='contentCategory')
    cta_button_text = sgqlc.types.Field(String, graphql_name='ctaButtonText')
    cta_link = sgqlc.types.Field(String, graphql_name='ctaLink')
    cta_second_button_text = sgqlc.types.Field(String, graphql_name='ctaSecondButtonText')
    cta_second_link = sgqlc.types.Field(String, graphql_name='ctaSecondLink')
    image = sgqlc.types.Field(Image, graphql_name='image')
    url = sgqlc.types.Field(String, graphql_name='url')


class Property(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('display_name', 'domain', 'franchises', 'full_name', 'identifier', 'property_type', 'enabled')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    franchises = sgqlc.types.Field(sgqlc.types.list_of(Franchise), graphql_name='franchises')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    property_type = sgqlc.types.Field(PropertyType, graphql_name='propertyType')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')


class Prospect(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('arm_length', 'background_image', 'bottom_line', 'college_class', 'college_conference', 'college_experience', 'college_jersey_number', 'colleges', 'combine_data', 'current_college', 'display_hint', 'draft', 'draft_pick', 'draft_position', 'draft_projection', 'draft_round', 'draft_year', 'elias_college_id', 'grade', 'grade_rubric', 'hand_size', 'headshot', 'height', 'home_state', 'meta_data', 'nfl_comparison', 'overview', 'person', 'position', 'position_depth', 'position_group', 'profile_author', 'sources_tell_us', 'strengths', 'video', 'weaknesses', 'weight', 'year', 'years_of_eligibility_left')
    arm_length = sgqlc.types.Field(String, graphql_name='armLength')
    background_image = sgqlc.types.Field(Image, graphql_name='backgroundImage')
    bottom_line = sgqlc.types.Field(String, graphql_name='bottomLine')
    college_class = sgqlc.types.Field(String, graphql_name='collegeClass')
    college_conference = sgqlc.types.Field(String, graphql_name='collegeConference')
    college_experience = sgqlc.types.Field(Int, graphql_name='collegeExperience')
    college_jersey_number = sgqlc.types.Field(String, graphql_name='collegeJerseyNumber')
    colleges = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='colleges')
    combine_data = sgqlc.types.Field(CombineData, graphql_name='combineData')
    current_college = sgqlc.types.Field(String, graphql_name='currentCollege')
    display_hint = sgqlc.types.Field(DisplayHint, graphql_name='displayHint')
    draft = sgqlc.types.Field(Draft, graphql_name='draft')
    draft_pick = sgqlc.types.Field(DraftPick, graphql_name='draftPick')
    draft_position = sgqlc.types.Field(Int, graphql_name='draftPosition')
    draft_projection = sgqlc.types.Field(String, graphql_name='draftProjection')
    draft_round = sgqlc.types.Field(Int, graphql_name='draftRound')
    draft_year = sgqlc.types.Field(Int, graphql_name='draftYear')
    elias_college_id = sgqlc.types.Field(Int, graphql_name='eliasCollegeId')
    grade = sgqlc.types.Field(Float, graphql_name='grade')
    grade_rubric = sgqlc.types.Field(String, graphql_name='gradeRubric')
    hand_size = sgqlc.types.Field(String, graphql_name='handSize')
    headshot = sgqlc.types.Field(Image, graphql_name='headshot')
    height = sgqlc.types.Field(String, graphql_name='height')
    home_state = sgqlc.types.Field(String, graphql_name='homeState')
    meta_data = sgqlc.types.Field(sgqlc.types.list_of(Meta), graphql_name='metaData', args=sgqlc.types.ArgDict((
        ('property_id', sgqlc.types.Arg(String, graphql_name='propertyId', default=None)),
))
    )
    nfl_comparison = sgqlc.types.Field(String, graphql_name='nflComparison')
    overview = sgqlc.types.Field(String, graphql_name='overview')
    person = sgqlc.types.Field(PlayerPerson, graphql_name='person')
    position = sgqlc.types.Field(String, graphql_name='position')
    position_depth = sgqlc.types.Field(Int, graphql_name='positionDepth')
    position_group = sgqlc.types.Field(PositionGroup, graphql_name='positionGroup')
    profile_author = sgqlc.types.Field(String, graphql_name='profileAuthor')
    sources_tell_us = sgqlc.types.Field(String, graphql_name='sourcesTellUs')
    strengths = sgqlc.types.Field(String, graphql_name='strengths')
    video = sgqlc.types.Field('Video', graphql_name='video')
    weaknesses = sgqlc.types.Field(String, graphql_name='weaknesses')
    weight = sgqlc.types.Field(String, graphql_name='weight')
    year = sgqlc.types.Field(Int, graphql_name='year')
    years_of_eligibility_left = sgqlc.types.Field(Int, graphql_name='yearsOfEligibilityLeft')


class ScoringSummary(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('clock_time', 'game_detail_id', 'home_score', 'pat_play_id', 'play_description', 'play_id', 'quarter', 'score_type', 'scoring_play_id', 'scoring_team', 'sequence', 'visitor_score')
    clock_time = sgqlc.types.Field(String, graphql_name='clockTime')
    game_detail_id = sgqlc.types.Field(String, graphql_name='gameDetailId')
    home_score = sgqlc.types.Field(Int, graphql_name='homeScore')
    pat_play_id = sgqlc.types.Field(Int, graphql_name='patPlayId')
    play_description = sgqlc.types.Field(String, graphql_name='playDescription')
    play_id = sgqlc.types.Field(Int, graphql_name='playId')
    quarter = sgqlc.types.Field(Int, graphql_name='quarter')
    score_type = sgqlc.types.Field(String, graphql_name='scoreType')
    scoring_play_id = sgqlc.types.Field(Int, graphql_name='scoringPlayId')
    scoring_team = sgqlc.types.Field('Team', graphql_name='scoringTeam')
    sequence = sgqlc.types.Field(Int, graphql_name='sequence')
    visitor_score = sgqlc.types.Field(Int, graphql_name='visitorScore')


class Season(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('season', 'teams', 'weeks')
    season = sgqlc.types.Field(Int, graphql_name='season')
    teams = sgqlc.types.Field(sgqlc.types.list_of('Team'), graphql_name='teams')
    weeks = sgqlc.types.Field(sgqlc.types.list_of('Week'), graphql_name='weeks')


class Series(sgqlc.types.Type, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('advertiser_frequency', 'advertiser_id', 'advertiser_text', 'pinned_content_ids', 'property', 'series_theme', 'thumbnail_image', 'title', 'type')
    advertiser_frequency = sgqlc.types.Field(Int, graphql_name='advertiserFrequency')
    advertiser_id = sgqlc.types.Field(String, graphql_name='advertiserId')
    advertiser_text = sgqlc.types.Field(String, graphql_name='advertiserText')
    pinned_content_ids = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='pinnedContentIds')
    property = sgqlc.types.Field(Property, graphql_name='property')
    series_theme = sgqlc.types.Field(String, graphql_name='seriesTheme')
    thumbnail_image = sgqlc.types.Field(Image, graphql_name='thumbnailImage')
    title = sgqlc.types.Field(String, graphql_name='title')
    type = sgqlc.types.Field(SeriesType, graphql_name='type')


class ShieldSearchContentPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('content',)
    content = sgqlc.types.Field(Content, graphql_name='content')


class ShieldSearchKeyValuePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('key_value',)
    key_value = sgqlc.types.Field(KeyValue, graphql_name='keyValue')


class ShieldSearchResult(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('content_type', 'image_id', 'keyword', 'last_modified', 'last_publish_date', 'metadata', 'original_publish_date', 'season', 'slug', 'summary', 'tags', 'title', 'url')
    content_type = sgqlc.types.Field(ContentType, graphql_name='contentType')
    image_id = sgqlc.types.Field(String, graphql_name='imageId')
    keyword = sgqlc.types.Field(String, graphql_name='keyword')
    last_modified = sgqlc.types.Field(DateTime, graphql_name='lastModified')
    last_publish_date = sgqlc.types.Field(DateTime, graphql_name='lastPublishDate')
    metadata = sgqlc.types.Field(Map, graphql_name='metadata')
    original_publish_date = sgqlc.types.Field(DateTime, graphql_name='originalPublishDate')
    season = sgqlc.types.Field(Int, graphql_name='season')
    slug = sgqlc.types.Field(String, graphql_name='slug')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    title = sgqlc.types.Field(String, graphql_name='title')
    url = sgqlc.types.Field(String, graphql_name='url')


class Show(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('name', 'property', 'workflow_status')
    name = sgqlc.types.Field(String, graphql_name='name')
    property = sgqlc.types.Field(Property, graphql_name='property')
    workflow_status = sgqlc.types.Field(WorkflowStatus, graphql_name='workflowStatus')


class Social(sgqlc.types.Type, AbstractAuditable):
    __schema__ = shield
    __field_names__ = ('label', 'link', 'platform')
    label = sgqlc.types.Field(String, graphql_name='label')
    link = sgqlc.types.Field(String, graphql_name='link')
    platform = sgqlc.types.Field(String, graphql_name='platform')


class Standings(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('team_records', 'week')
    team_records = sgqlc.types.Field(sgqlc.types.list_of('TeamRecord'), graphql_name='teamRecords')
    week = sgqlc.types.Field('Week', graphql_name='week')


class Tag(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('advertiser_id', 'property', 'tag')
    advertiser_id = sgqlc.types.Field(String, graphql_name='advertiserId')
    property = sgqlc.types.Field(Property, graphql_name='property')
    tag = sgqlc.types.Field(String, graphql_name='tag')


class Team(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('abbreviation', 'city_state_region', 'coaches', 'conference', 'division', 'franchise', 'full_name', 'injuries', 'league', 'logo', 'market_zip_code', 'nick_name', 'players', 'season', 'season_value', 'team_type', 'venues')
    abbreviation = sgqlc.types.Field(String, graphql_name='abbreviation')
    city_state_region = sgqlc.types.Field(String, graphql_name='cityStateRegion')
    coaches = sgqlc.types.Field(sgqlc.types.list_of(Coach), graphql_name='coaches')
    conference = sgqlc.types.Field(Conference, graphql_name='conference')
    division = sgqlc.types.Field(Division, graphql_name='division')
    franchise = sgqlc.types.Field(Franchise, graphql_name='franchise')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(Injury), graphql_name='injuries')
    league = sgqlc.types.Field(League, graphql_name='league')
    logo = sgqlc.types.Field(Image, graphql_name='logo')
    market_zip_code = sgqlc.types.Field(String, graphql_name='marketZipCode')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    players = sgqlc.types.Field(sgqlc.types.list_of(Player), graphql_name='players')
    season = sgqlc.types.Field(Season, graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_type = sgqlc.types.Field(TeamType, graphql_name='teamType')
    venues = sgqlc.types.Field(sgqlc.types.list_of('Venue'), graphql_name='venues')


class TeamGameStats(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('game', 'opponent_game_stats', 'season', 'season_value', 'team', 'team_game_stats', 'week')
    game = sgqlc.types.Field(Game, graphql_name='game')
    opponent_game_stats = sgqlc.types.Field(TeamGameStatsDetail, graphql_name='opponentGameStats')
    season = sgqlc.types.Field(Season, graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team = sgqlc.types.Field(Team, graphql_name='team')
    team_game_stats = sgqlc.types.Field(TeamGameStatsDetail, graphql_name='teamGameStats')
    week = sgqlc.types.Field('Week', graphql_name='week')


class TeamOnBye(sgqlc.types.Type, Node):
    __schema__ = shield
    __field_names__ = ('abbreviation', 'city_state_region', 'coaches', 'conference', 'created_date', 'division', 'franchise', 'full_name', 'injuries', 'last_modified_date', 'league', 'logo', 'market_zip_code', 'next_matchup_team', 'nick_name', 'players', 'season', 'season_value', 'team_type', 'venues')
    abbreviation = sgqlc.types.Field(String, graphql_name='abbreviation')
    city_state_region = sgqlc.types.Field(String, graphql_name='cityStateRegion')
    coaches = sgqlc.types.Field(sgqlc.types.list_of(Coach), graphql_name='coaches')
    conference = sgqlc.types.Field(Conference, graphql_name='conference')
    created_date = sgqlc.types.Field(DateTime, graphql_name='createdDate')
    division = sgqlc.types.Field(Division, graphql_name='division')
    franchise = sgqlc.types.Field(Franchise, graphql_name='franchise')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    injuries = sgqlc.types.Field(sgqlc.types.list_of(Injury), graphql_name='injuries')
    last_modified_date = sgqlc.types.Field(DateTime, graphql_name='lastModifiedDate')
    league = sgqlc.types.Field(League, graphql_name='league')
    logo = sgqlc.types.Field(Image, graphql_name='logo')
    market_zip_code = sgqlc.types.Field(String, graphql_name='marketZipCode')
    next_matchup_team = sgqlc.types.Field(Team, graphql_name='nextMatchupTeam')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    players = sgqlc.types.Field(sgqlc.types.list_of(Player), graphql_name='players')
    season = sgqlc.types.Field(Season, graphql_name='season')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team_type = sgqlc.types.Field(TeamType, graphql_name='teamType')
    venues = sgqlc.types.Field(sgqlc.types.list_of('Venue'), graphql_name='venues')


class TeamRecord(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('clinch_division', 'clinch_division_and_homefield', 'clinch_playoff', 'clinch_wc', 'conference', 'conference_loss', 'conference_pct', 'conference_pts_against', 'conference_pts_for', 'conference_rank', 'conference_tie', 'conference_week_high', 'conference_week_low', 'conference_win', 'division', 'division_loss', 'division_pct', 'division_pts_against', 'division_pts_for', 'division_rank', 'division_tie', 'division_week_high', 'division_week_low', 'division_win', 'eliminated_from_postseason', 'final_week', 'franchise_id', 'full_name', 'home_loss', 'home_pct', 'home_pts_against', 'home_pts_for', 'home_tie', 'home_win', 'last5_loss', 'last5_pct', 'last5_pts_against', 'last5_pts_for', 'last5_tie', 'last5_win', 'nick_name', 'overall_loss', 'overall_pct', 'overall_pts_against', 'overall_pts_for', 'overall_streak', 'overall_tie', 'overall_week_high', 'overall_week_low', 'overall_win', 'road_loss', 'road_pct', 'road_pts_against', 'road_pts_for', 'road_tie', 'road_win', 'team_id', 'week_id')
    clinch_division = sgqlc.types.Field(Boolean, graphql_name='clinchDivision')
    clinch_division_and_homefield = sgqlc.types.Field(Boolean, graphql_name='clinchDivisionAndHomefield')
    clinch_playoff = sgqlc.types.Field(Boolean, graphql_name='clinchPlayoff')
    clinch_wc = sgqlc.types.Field(Boolean, graphql_name='clinchWc')
    conference = sgqlc.types.Field(Conference, graphql_name='conference')
    conference_loss = sgqlc.types.Field(Int, graphql_name='conferenceLoss')
    conference_pct = sgqlc.types.Field(Float, graphql_name='conferencePct')
    conference_pts_against = sgqlc.types.Field(Int, graphql_name='conferencePtsAgainst')
    conference_pts_for = sgqlc.types.Field(Int, graphql_name='conferencePtsFor')
    conference_rank = sgqlc.types.Field(Int, graphql_name='conferenceRank')
    conference_tie = sgqlc.types.Field(Int, graphql_name='conferenceTie')
    conference_week_high = sgqlc.types.Field(Int, graphql_name='conferenceWeekHigh')
    conference_week_low = sgqlc.types.Field(Int, graphql_name='conferenceWeekLow')
    conference_win = sgqlc.types.Field(Int, graphql_name='conferenceWin')
    division = sgqlc.types.Field(Division, graphql_name='division')
    division_loss = sgqlc.types.Field(Int, graphql_name='divisionLoss')
    division_pct = sgqlc.types.Field(Float, graphql_name='divisionPct')
    division_pts_against = sgqlc.types.Field(Int, graphql_name='divisionPtsAgainst')
    division_pts_for = sgqlc.types.Field(Int, graphql_name='divisionPtsFor')
    division_rank = sgqlc.types.Field(Int, graphql_name='divisionRank')
    division_tie = sgqlc.types.Field(Int, graphql_name='divisionTie')
    division_week_high = sgqlc.types.Field(Int, graphql_name='divisionWeekHigh')
    division_week_low = sgqlc.types.Field(Int, graphql_name='divisionWeekLow')
    division_win = sgqlc.types.Field(Int, graphql_name='divisionWin')
    eliminated_from_postseason = sgqlc.types.Field(Boolean, graphql_name='eliminatedFromPostseason')
    final_week = sgqlc.types.Field(String, graphql_name='finalWeek')
    franchise_id = sgqlc.types.Field(String, graphql_name='franchiseId')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    home_loss = sgqlc.types.Field(Int, graphql_name='homeLoss')
    home_pct = sgqlc.types.Field(Float, graphql_name='homePct')
    home_pts_against = sgqlc.types.Field(Int, graphql_name='homePtsAgainst')
    home_pts_for = sgqlc.types.Field(Int, graphql_name='homePtsFor')
    home_tie = sgqlc.types.Field(Int, graphql_name='homeTie')
    home_win = sgqlc.types.Field(Int, graphql_name='homeWin')
    last5_loss = sgqlc.types.Field(Int, graphql_name='last5Loss')
    last5_pct = sgqlc.types.Field(Float, graphql_name='last5Pct')
    last5_pts_against = sgqlc.types.Field(Int, graphql_name='last5PtsAgainst')
    last5_pts_for = sgqlc.types.Field(Int, graphql_name='last5PtsFor')
    last5_tie = sgqlc.types.Field(Int, graphql_name='last5Tie')
    last5_win = sgqlc.types.Field(Int, graphql_name='last5Win')
    nick_name = sgqlc.types.Field(String, graphql_name='nickName')
    overall_loss = sgqlc.types.Field(Int, graphql_name='overallLoss')
    overall_pct = sgqlc.types.Field(Float, graphql_name='overallPct')
    overall_pts_against = sgqlc.types.Field(Int, graphql_name='overallPtsAgainst')
    overall_pts_for = sgqlc.types.Field(Int, graphql_name='overallPtsFor')
    overall_streak = sgqlc.types.Field(String, graphql_name='overallStreak')
    overall_tie = sgqlc.types.Field(Int, graphql_name='overallTie')
    overall_week_high = sgqlc.types.Field(Int, graphql_name='overallWeekHigh')
    overall_week_low = sgqlc.types.Field(Int, graphql_name='overallWeekLow')
    overall_win = sgqlc.types.Field(Int, graphql_name='overallWin')
    road_loss = sgqlc.types.Field(Int, graphql_name='roadLoss')
    road_pct = sgqlc.types.Field(Float, graphql_name='roadPct')
    road_pts_against = sgqlc.types.Field(Int, graphql_name='roadPtsAgainst')
    road_pts_for = sgqlc.types.Field(Int, graphql_name='roadPtsFor')
    road_tie = sgqlc.types.Field(Int, graphql_name='roadTie')
    road_win = sgqlc.types.Field(Int, graphql_name='roadWin')
    team_id = sgqlc.types.Field(String, graphql_name='teamId')
    week_id = sgqlc.types.Field(String, graphql_name='weekId')


class TeamStats(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('opponent_season_stats', 'season', 'season_type', 'season_value', 'team', 'team_season_stats', 'team_split_stats')
    opponent_season_stats = sgqlc.types.Field(TeamSeasonStatsDetail, graphql_name='opponentSeasonStats')
    season = sgqlc.types.Field(Season, graphql_name='season')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    team = sgqlc.types.Field(Team, graphql_name='team')
    team_season_stats = sgqlc.types.Field(TeamSeasonStatsDetail, graphql_name='teamSeasonStats')
    team_split_stats = sgqlc.types.Field(sgqlc.types.list_of(TeamSeasonSplitStatsDetail), graphql_name='teamSplitStats')


class UpdateFranchisePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('franchise',)
    franchise = sgqlc.types.Field(Franchise, graphql_name='franchise')


class UpdateGamePayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('game',)
    game = sgqlc.types.Field(Game, graphql_name='game')


class UpdatePlayerPersonPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('player_person',)
    player_person = sgqlc.types.Field(PlayerPerson, graphql_name='playerPerson')


class UpdateTeamPayload(sgqlc.types.Type, RelayMutationType):
    __schema__ = shield
    __field_names__ = ('team',)
    team = sgqlc.types.Field(Team, graphql_name='team')


class Venue(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('city', 'country', 'display_name', 'full_name', 'postal_code', 'state')
    city = sgqlc.types.Field(String, graphql_name='city')
    country = sgqlc.types.Field(String, graphql_name='country')
    display_name = sgqlc.types.Field(String, graphql_name='displayName')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    postal_code = sgqlc.types.Field(String, graphql_name='postalCode')
    state = sgqlc.types.Field(String, graphql_name='state')


class Video(sgqlc.types.Type, AbstractContent, AbstractPublishable, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('clip_type', 'event_occurred_date', 'image', 'pre_roll_enabled', 'primary_channel', 'related_plays', 'series_list', 'video_asset', 'week')
    clip_type = sgqlc.types.Field(ClipType, graphql_name='clipType')
    event_occurred_date = sgqlc.types.Field(DateTime, graphql_name='eventOccurredDate')
    image = sgqlc.types.Field(Image, graphql_name='image')
    pre_roll_enabled = sgqlc.types.Field(Boolean, graphql_name='preRollEnabled')
    primary_channel = sgqlc.types.Field(String, graphql_name='primaryChannel')
    related_plays = sgqlc.types.Field(sgqlc.types.list_of(Play), graphql_name='relatedPlays')
    series_list = sgqlc.types.Field(sgqlc.types.list_of(Series), graphql_name='seriesList')
    video_asset = sgqlc.types.Field('VideoAsset', graphql_name='videoAsset')
    week = sgqlc.types.Field('Week', graphql_name='week')


class VideoAsset(sgqlc.types.Type, AbstractAsset, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('bitrates', 'closed_captions_url', 'encoding_date', 'image', 'music', 'playback_url', 'runtime_secs', 'closed_captions_embedded')
    bitrates = sgqlc.types.Field(sgqlc.types.list_of(Bitrate), graphql_name='bitrates')
    closed_captions_url = sgqlc.types.Field(String, graphql_name='closedCaptionsUrl')
    encoding_date = sgqlc.types.Field(DateTime, graphql_name='encodingDate')
    image = sgqlc.types.Field(Image, graphql_name='image')
    music = sgqlc.types.Field(sgqlc.types.list_of(Music), graphql_name='music')
    playback_url = sgqlc.types.Field(String, graphql_name='playbackUrl')
    runtime_secs = sgqlc.types.Field(Int, graphql_name='runtimeSecs')
    closed_captions_embedded = sgqlc.types.Field(Boolean, graphql_name='closedCaptionsEmbedded')


class Weather(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('current_fahrenheit', 'current_real_feel_fahrenheit', 'high_fahrenheit', 'high_real_feel_fahrenheit', 'location', 'long_description', 'low_fahrenheit', 'low_real_feel_fahrenheit', 'observe_date', 'short_description', 'visibility_miles', 'wind_direction', 'wind_gust_mph', 'wind_speed_mph')
    current_fahrenheit = sgqlc.types.Field(Int, graphql_name='currentFahrenheit')
    current_real_feel_fahrenheit = sgqlc.types.Field(Int, graphql_name='currentRealFeelFahrenheit')
    high_fahrenheit = sgqlc.types.Field(Int, graphql_name='highFahrenheit')
    high_real_feel_fahrenheit = sgqlc.types.Field(Int, graphql_name='highRealFeelFahrenheit')
    location = sgqlc.types.Field(String, graphql_name='location')
    long_description = sgqlc.types.Field(String, graphql_name='longDescription')
    low_fahrenheit = sgqlc.types.Field(Int, graphql_name='lowFahrenheit')
    low_real_feel_fahrenheit = sgqlc.types.Field(Int, graphql_name='lowRealFeelFahrenheit')
    observe_date = sgqlc.types.Field(DateTime, graphql_name='observeDate')
    short_description = sgqlc.types.Field(String, graphql_name='shortDescription')
    visibility_miles = sgqlc.types.Field(Int, graphql_name='visibilityMiles')
    wind_direction = sgqlc.types.Field(String, graphql_name='windDirection')
    wind_gust_mph = sgqlc.types.Field(Int, graphql_name='windGustMph')
    wind_speed_mph = sgqlc.types.Field(Int, graphql_name='windSpeedMph')


class Week(sgqlc.types.Type, AbstractEntity, AbstractAuditable, Node):
    __schema__ = shield
    __field_names__ = ('date_begin', 'date_end', 'season', 'season_type', 'season_value', 'week_order', 'week_type', 'week_value')
    date_begin = sgqlc.types.Field(DateTime, graphql_name='dateBegin')
    date_end = sgqlc.types.Field(DateTime, graphql_name='dateEnd')
    season = sgqlc.types.Field(Season, graphql_name='season')
    season_type = sgqlc.types.Field(SeasonType, graphql_name='seasonType')
    season_value = sgqlc.types.Field(Int, graphql_name='seasonValue')
    week_order = sgqlc.types.Field(Int, graphql_name='weekOrder')
    week_type = sgqlc.types.Field(WeekType, graphql_name='weekType')
    week_value = sgqlc.types.Field(Int, graphql_name='weekValue')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
shield.query_type = Viewer
shield.mutation_type = Mutation
shield.subscription_type = None

