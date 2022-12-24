from pprint import pprint

import logging
from typing import List, Tuple, Dict

import dotenv
import asyncio
import os
import json
from vkbottle import User

logger = logging.getLogger()
logger.setLevel('INFO')


async def get_accounts_data() -> List[List]:
    """ Импорт данных аккаунтов из .env
    :return: [['89102000303', 'password'], ['888888888', 'qwerty']]
    """

    dotenv.load_dotenv('.env')
    vk_accounts = json.loads(os.getenv('vk_accounts'))
    accounts_list = []
    for account in vk_accounts:
        data = account.replace(' ', '').split(',')
        accounts_list.append(data)
    return accounts_list


class VkUserBot:

    def __init__(self, login, password):
        self.login = login
        self.password = password

    async def get_recommendations(self, news_count=100) -> List[Dict]:

        """Получение рекомендаций
        :news_count: количество получаемых постов
        """

        self.user = await User.direct_auth(login=self.login, password=self.password)

        response = await self.user.api.request("newsfeed.getRecommended", data={'count': news_count})
        response = response.get('response')
        groups = response.get('groups')
        items = response.get('items')

        data = list()

        for group in groups:
            group_data = dict()
            group_data['group_id'] = str(group.get('id'))
            group_data['name'] = group.get('name')
            group_data['link'] = f'https://vk.com/public{group.get("id")}'

            group_info = await self.user.api.groups.get_by_id(group_id=group_data['group_id'],
                                                              fields='activity, description')

            group_data['activity'] = group_info[0].activity
            group_data['description'] = group_info[0].description

            data.append(group_data)

        for item in items:
            if item.get('account_import_block_pos'):
                continue
            post = dict()
            post['post_id'] = item.get('post_id')
            post['group_id'] = str(item.get('owner_id')).replace('-', '')
            post['text'] = item.get('text')
            post['date'] = item.get('date')
            category_action = item.get('category_action')
            if category_action:
                category = category_action.get('name')
            else:
                category = None
            post['category'] = category
            post['views'] = item.get('views')
            post['reposts'] = item.get('reposts')
            post['likes'] = item.get('likes')
            post['comments'] = item.get('comments')

            # attachments = item.get('attachments')
            # for attachment in attachments:
            #     attachment_data = dict()
            #     type = attachment.get('type')
            #     attachment_data['type'] = type
            #     if type == 'video':
            #         video = attachment.get('video')
            #         attachment_data['description'] = video.get('description')
            #         attachment_data['title'] = video.get('title')

            for group in data:
                if group['group_id'] == post['group_id']:
                    group['post'] = post

        return data

    async def like_post(self, posts_info: List[Tuple]):
        """
        Лайк множества постов
        :posts_info: [(post_id, group_id), (post_id, group_id),...]
        :return
        """
        self.user = await User.direct_auth(login=self.login, password=self.password)

        for post in posts_info:
            post_id = post[0]
            owner_id = post[1]

            await self.user.api.likes.add(type='post', item_id=post_id, owner_id=f'-{owner_id}')

    async def group_join(self, groups_ids: List):
        """
        Вступление в множество групп
        :param groups_ids: [group_id1, group_id2,...]
        :return:
        """
        self.user = await User.direct_auth(login=self.login, password=self.password)
        for group_id in groups_ids:
            await self.user.api.groups.join(group_id=group_id)


if __name__ == '__main__':
    bot = VkUserBot(login='89259922019', password='gibsoncsv16xp')
    #
    # data = asyncio.run(bot.get_recommendations(news_count=2))

    # groups = []
    # for post in data:
    #     groups.append(post.get('group_id'))
    # asyncio.run(bot.group_join(groups))

    # for post in data:
    #     q = post.get('post')
    #     post_id = q.get('post_id')
    #     group_id = q.get('group_id')
    #     info = [(post_id, group_id)]
    #     asyncio.run(bot.like_post(info))
