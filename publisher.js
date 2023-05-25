const amqp = require('amqplib');
const amqpUrl = process.env.AMQP_URL || 'amqp://localhost:5673';

// RabbitMQ configuration
const exchange = 'file_upload';
const queue = 'file_upload_queue';
const routingKey = 'file_uploaded';

async function sendMessage(message) {
  try {
    const connection = await amqp.connect(amqpUrl);
    const channel = await connection.createChannel();

    await channel.assertExchange(exchange, 'direct', { durable: true });
    await channel.assertQueue(queue, { durable: true });
    await channel.bindQueue(queue, exchange, routingKey);

    await channel.publish(exchange, routingKey, Buffer.from(JSON.stringify(message)));

    await channel.close();
    await connection.close();
  } catch (error) {
    throw new Error('Error sending message to RabbitMQ');
  }
}

module.exports = { sendMessage };
