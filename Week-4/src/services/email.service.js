import nodemailer from 'nodemailer';
import logger from '../utils/logger.js';

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'ishaansahu2030@gmail.com',
    pass: 'oznudshytilyxtvj', 
  },
});

export const sendWelcomeEmail = async (userData) => {
  const { firstName, lastName, email, createdAt } = userData;

  const htmlContent = `
    <h1>Welcome to the Platform, ${firstName}!</h1>
    <p>Here are your registered details:</p>
    <table border="1" style="border-collapse: collapse; width: 100%;">
      <thead>
        <tr style="background-color: #f2f2f2;">
          <th style="padding: 10px; text-align: left;">Field</th>
          <th style="padding: 10px; text-align: left;">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr><td style="padding: 10px;">Full Name</td><td style="padding: 10px;">${firstName} ${lastName}</td></tr>
        <tr><td style="padding: 10px;">Email</td><td style="padding: 10px;">${email}</td></tr>
        <tr><td style="padding: 10px;">Joined On</td><td style="padding: 10px;">${new Date(createdAt).toLocaleDateString()}</td></tr>
      </tbody>
    </table>
  `;

    try {
        const info = await transporter.sendMail({
        from: `Ishaan Sahu HestaBit`,
        to: email,
        subject: "Welcome! Your Account Details",
        html: htmlContent,
        });
        
        logger.info(`Email sent successfully: ${info.messageId}`);
        return info;
    } catch (error) {
        logger.error(`Nodemailer Error: ${error.message}`);
        throw error;
  }
};