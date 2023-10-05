import datetime
import io
from typing import List, Optional

import interactions as ipy
from chat_exporter.construct.transcript import Transcript



async def quick_export(
    channel: ipy.GuildText,
    bot: Optional[ipy.Client] = None,
):
    """
    Create a quick export of your Discord channel.
    This function will produce the transcript and post it back in to your channel.
    :param channel: interactions.GuildText
    :param bot: (optional) interactions.Client
    :return: interactions.Message (posted transcript)
    """

    transcript = (
        await Transcript(
            channel=channel,
            limit=None,
            messages=None,
            pytz_timezone="UTC",
            military_time=True,
            fancy_times=True,
            before=None,
            after=None,
            support_dev=True,
            bot=bot,
            ).export()
        ).html

    if not transcript:
        return

    transcript_embed = ipy.Embed(
        description=f"**Transcript Name:** transcript-{channel.name}\n\n",
        color=ipy.BrandColors.BLURPLE,
    )

    transcript_file = ipy.File(io.BytesIO(transcript.encode()), file_name=f"transcript-{channel.name}.html")
    return await channel.send(embed=transcript_embed, file=transcript_file)


async def export(
    channel: ipy.GuildText,
    limit: Optional[int] = None,
    tz_info="UTC",
    bot: Optional[ipy.Client] = None,
    military_time: Optional[bool] = True,
    fancy_times: Optional[bool] = True,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
    support_dev: Optional[bool] = True,
):
    """
    Create a customised transcript of your Discord channel.
    This function will return the transcript which you can then turn in to a file to post wherever.
    :param channel: interactions.GuildText - channel to Export
    :param limit: (optional) integer - limit of messages to capture
    :param tz_info: (optional) TZ Database Name - set the timezone of your transcript
    :param bot: (optional) interactions.Client - set getting member role colour
    :param military_time: (optional) boolean - set military time (24hour clock)
    :param fancy_times: (optional) boolean - set javascript around time display
    :param before: (optional) datetime.datetime - allows before time for history
    :param after: (optional) datetime.datetime - allows after time for history
    :return: string - transcript file make up
    """

    return (
        await Transcript(
            channel=channel,
            limit=limit,
            messages=None,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=before,
            after=after,
            support_dev=support_dev,
            bot=bot,
        ).export()
    ).html


async def raw_export(
    channel: ipy.GuildText,
    messages: List[ipy.Message],
    tz_info="UTC",
    bot: Optional[ipy.Client] = None,
    military_time: Optional[bool] = False,
    fancy_times: Optional[bool] = True,
    support_dev: Optional[bool] = True,
):
    """
    Create a customised transcript with your own captured Discord messages
    This function will return the transcript which you can then turn in to a file to post wherever.
    :param channel: interactions.GuildText - channel to Export
    :param messages: List[interactions.Message] - list of Discord messages to export
    :param tz_info: (optional) TZ Database Name - set the timezone of your transcript
    :param bot: (optional) interactions.Client - set getting member role colour
    :param military_time: (optional) boolean - set military time (24hour clock)
    :param fancy_times: (optional) boolean - set javascript around time display
    :return: string - transcript file make up
    """
    return (
        await Transcript(
            channel=channel,
            limit=None,
            messages=messages,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=None,
            after=None,
            support_dev=support_dev,
            bot=bot,
        ).export()
    ).html


async def quick_link(
    channel: ipy.GuildText,
    message: ipy.Message
):
    """
    Create a quick link for your transcript file.
    This function will return an embed with a link to view the transcript online.
    :param channel: interactions.TextChannel
    :param message: interactions.Message
    :return: interactions.Message (posted link)
    """
    embed = ipy.Embed(
        title="Transcript Link",
        description=(
            f"[Click here to view the transcript](https://mahto.id/chat-exporter?url={message.attachments[0].url})"
        ),
        color=ipy.BrandColors.BLURPLE,
    )

    return await channel.send(embed=embed)


async def link(
    message: ipy.Message
):
    """
    Returns a link which you can use to display in a message.
    This function will return a string of the link.
    :param message: interactions.Message
    :return: string (link: https://mahto.id/chat-exporter?url=ATTACHMENT_URL)
    """
    return "https://mahto.id/chat-exporter?url=" + message.attachments[0].url
