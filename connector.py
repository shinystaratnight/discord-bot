import mysql.connector

class Connector:
    def __init__(self, config):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def __del__(self):
        if hasattr(self, 'cnx') and self.cnx:
            self.cnx.close()
            
    async def fetch_user(self, client_id):
        cursor = self.cnx.cursor(buffered=True)
        select_user_query = ("SELECT * FROM users "
                            "WHERE id=%s")
        cursor.execute(select_user_query, (client_id,))
        user = {}
        for (id, experience, level) in cursor:
            user['id'] = id
            user['experience'] = experience
            user['level'] = level
            
        cursor.close()
        return user
    
    async def user_already_registered(self, client_id):
        cursor = self.cnx.cursor(buffered=True)
        select_user_query = ("SELECT * FROM users "
                            "WHERE id=%s")
        cursor.execute(select_user_query, (client_id,))
        return_code = cursor.rowcount
        cursor.close()
        
        return True if return_code else False
    
    async def register_user(self, client_id):
        if not await self.user_already_registered(client_id):
            cursor = self.cnx.cursor()
            register_user_query = ("INSERT INTO users"
                                   "(id)"
                                   " VALUES (%s)")
            cursor.execute(register_user_query, (client_id,))
            self.cnx.commit()
            cursor.close()
        else:
            pass
        return
        
    async def update_user(self, message):
        user = await self.fetch_user(message.author.id)
        user['experience'] = int(user['experience']) + 2
        new_rank = int(user['experience'] ** (1 / 4))
        
        if new_rank > int(user['level']):
            await message.channel.send('{} has leveled up to level {}'.format(message.author.mention, new_rank))
        cursor = self.cnx.cursor()
        update_user_query = ("UPDATE users"
                             " SET experience=%s, level=%s"
                             " WHERE id=%s")
        cursor.execute(update_user_query, (user['experience'], new_rank, message.author.id))
        self.cnx.commit()
        cursor.close()