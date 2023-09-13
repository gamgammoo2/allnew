import { NestFactory } from '@nestjs/core';
import { Appmodule } from './app/app.module';

async function bootstrap() {
    const app = await NestFactory.create(Appmodule);
    app.setGlobalPrefix('./api');
    await app.listen(3000);
}
bootstrap();